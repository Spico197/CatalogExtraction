from pathlib import Path

from omegaconf import OmegaConf
import torch
import torch.optim as optim
from transformers import BertTokenizerFast
from rex.utils.logging import logger
from rex.utils.io import dump_json, load_json
from rex.data.dataset import CachedDataset
from rex.data.manager import CachedManager
from rex.utils.tensor_move import move_to_device
from rex.utils.progress_bar import tqdm
from rex.tasks.base_task import TaskBase
from rex.metrics.classification import mc_prf1

from doctree.data.transform.text_classification import (
    TextClassificationTransform,
    text_classification_collate_fn,
)
from doctree.models.text_classification import TextClassificationModel
from doctree.data.convert import convert_sent_list_to_node


class TextClassificationTask(TaskBase):
    def __init__(self, config: OmegaConf) -> None:
        super().__init__(config)

        self.middle_path = Path(self.config.task_dir).joinpath("middle")
        self.middle_path.mkdir(parents=True, exist_ok=True)

        tokenizer = BertTokenizerFast.from_pretrained(config.plm_dir)
        self.transform = TextClassificationTransform(tokenizer, self.config.max_seq_len)
        self.data_manager = CachedManager(
            config.train_filepath,
            config.dev_filepath,
            config.test_filepath,
            CachedDataset,
            self.transform,
            load_json,
            config.train_batch_size,
            config.eval_batch_size,
            text_classification_collate_fn,
            debug_mode=config.debug_mode,
            load_train_data=not config.skip_train,
            load_dev_data=not config.skip_train,
            load_test_data=not config.skip_final_eval,
        )
        self.model = TextClassificationModel(
            plm_filepath=config.plm_dir,
            num_filters=config.num_filters,
            num_classes=self.transform.label_encoder.num_tags,
            dropout=config.dropout,
            kernel_sizes=config.kernel_sizes,
            mid_dims=config.mid_dims,
        )
        self.model.to(self.config.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=config.learning_rate)

    def print_final_record(self):
        logger.info(
            (
                f"Best Epoch: {self.best_epoch}, Dev: {self.history['dev'][self.best_epoch]}, "
                f"Best Test: {self.history['test'][self.best_epoch]}"
            )
        )

    def train(self):
        for epoch_idx in range(self.config.num_epochs):
            logger.info(f"Epoch: {epoch_idx}/{self.config.num_epochs}")
            self.model.train()
            loader = tqdm(self.data_manager.train_loader, desc=f"Train(e{epoch_idx})")
            total_loss = 0.0
            train_num = 0.0
            for batch in loader:
                batch = move_to_device(batch, self.config.device)
                result = self.model(**batch)
                loss = result["loss"]
                logits = result["logits"]
                loader.set_postfix({"loss": loss.item()})
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item() * logits.shape[0]
                train_num += logits.shape[0]
            logger.info(loader)
            train_loss = total_loss / train_num
            train_measures = self.eval("train", verbose=True, postfix=f"{epoch_idx}")
            self.history["train"].append(train_measures)
            dev_measures = self.eval("dev", verbose=True, postfix=f"{epoch_idx}")
            self.history["dev"].append(dev_measures)
            test_measures = self.eval("test", verbose=True, postfix=f"{epoch_idx}")
            self.history["test"].append(test_measures)

            measures = dev_measures
            is_best = False
            if measures > self.best_metric:
                is_best = True
                self.best_metric = measures
                self.best_epoch = epoch_idx
                self.no_climbing_cnt = 0
            else:
                self.no_climbing_cnt += 1

            if is_best and self.config.save_best_ckpt:
                self.save_ckpt(f"{epoch_idx}.{100 * dev_measures:.3f}", epoch_idx)
                self.save_ckpt("best", epoch_idx)

            logger.info(
                (
                    f"Epoch: {epoch_idx}, is_best: {is_best}, "
                    f"Train_Loss: {train_loss}, "
                    f"Train: {100 * train_measures:.3f}, "
                    f"Dev: {100 * dev_measures:.3f}, "
                    f"Test: {100 * test_measures:.3f}"
                )
            )

            if (
                self.config.num_early_stop > 0
                and self.no_climbing_cnt > self.config.num_early_stop
            ):
                break

        logger.info("Trian finished.")
        self.print_final_record()

    @torch.no_grad()
    def eval(self, dataset_name: str, verbose=False, postfix=""):
        self.model.eval()
        name2loader = {
            "train": self.data_manager.train_eval_loader,
            "dev": self.data_manager.dev_loader,
            "test": self.data_manager.test_loader,
        }
        loader = tqdm(name2loader[dataset_name], desc=f"{dataset_name} Eval")
        preds = []
        golds = []
        dump_data = []
        for raw_batch in loader:
            raw_batch = move_to_device(raw_batch, self.config.device)
            golds.extend(raw_batch["labels"].cpu())
            outputs = self.model(**raw_batch)
            batch_pred_ = outputs["preds"].detach().tolist()
            preds.extend(batch_pred_)
            for text, gold, pred_ in zip(
                raw_batch["text"],
                raw_batch["labels"].detach().tolist(),
                batch_pred_,
            ):
                dump_data.append(
                    {
                        "text": text,
                        "gold": gold,
                        "pred": pred_,
                    }
                )

        logger.info(loader)
        cls_results = mc_prf1(
            preds,
            golds,
            num_classes=self.transform.label_encoder.num_tags,
            label_idx2name=self.transform.label_encoder.id2label,
        )
        if verbose:
            logger.info(f"{dataset_name} Eval Measures: {cls_results}")

        dump_json(
            dump_data, self.middle_path.joinpath(f"{dataset_name}.{postfix}.json")
        )
        return cls_results["micro"]["f1"]

    @torch.no_grad()
    def predict(self, texts):
        self.model.eval()
        texts_with_labels = []
        for text in texts:
            data = {"text": text}
            batch = self.transform.predict_transform(data)
            tensor_batch = self.data_manager.collate_fn([batch])
            tensor_batch = move_to_device(tensor_batch, self.config.device)
            outputs = self.model(**tensor_batch)
            pred_label_id = outputs["preds"].cpu().tolist()[0]
            pred_label = self.transform.label_encoder.id2label[pred_label_id]
            texts_with_labels.append({"text": text, "label": pred_label})
        root_node = convert_sent_list_to_node(texts_with_labels)
        return root_node, texts_with_labels
