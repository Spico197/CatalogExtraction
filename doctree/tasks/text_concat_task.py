import os
from pathlib import Path
from typing import List

from omegaconf import OmegaConf
import torch
import torch.optim as optim
from transformers import AutoTokenizer
from rex.utils.progress_bar import tqdm
from rex.utils.logging import logger
from rex.tasks.base_task import TaskBase
from rex.data.manager import CachedManager
from rex.data.dataset import CachedDataset
from rex.utils.io import dump_json, load_json
from rex.utils.tensor_move import move_to_device

from doctree.data.transform import TextConcatTransform
from doctree.data.transform.text_concat import text_concat_collate_fn
from doctree.models.text_concat import TextConcat
from doctree.utils import content_tool as C


class TextConcatTask(TaskBase):
    def __init__(self, config: OmegaConf, **kwargs) -> None:
        super().__init__(config, **kwargs)

        Path(config.score_dir).mkdir(parents=True, exist_ok=True)

        tokenizer = AutoTokenizer.from_pretrained(config.plm_dir)
        self.transform = TextConcatTransform(tokenizer, config.max_seq_len)
        self.data_manager = CachedManager(
            config.train_filepath,
            config.dev_filepath,
            config.test_filepath,
            CachedDataset,
            self.transform,
            load_json,
            config.train_batch_size,
            config.eval_batch_size,
            text_concat_collate_fn,
            debug_mode=config.debug_mode,
            load_train_data=config.load_train_data,
            load_dev_data=config.load_dev_data,
            load_test_data=config.load_test_data,
        )

        self.model = TextConcat(
            config.plm_dir, pred_threshold=config.pred_threshold, dropout=config.dropout
        )
        self.model.to(self.config.device)
        self.optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.config.learning_rate,
        )

    def train(self):
        for epoch_idx in range(0, self.config.num_epochs):
            self.model.train()
            loader = tqdm(
                self.data_manager.train_loader,
                desc=f"Train(e{epoch_idx}/{self.config.num_epochs})",
            )
            total_loss = 0.0
            train_num = 0.0
            for batch in loader:
                batch = move_to_device(batch, self.config.device)
                _ = batch.pop("raw_data")
                return_obj = self.model(**batch)
                logits = return_obj["logits"]
                loss = return_obj["loss"]

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item() * logits.shape[0]
                train_num += logits.shape[0]
            logger.info(loader)
            train_loss = total_loss / train_num

            acc, eval_loss, all_answer = self.eval("dev")
            self.history["dev"].append({"acc": acc, "loss": eval_loss})
            test_acc, test_eval_loss, test_all_answer = self.eval("test")
            self.history["test"].append({"acc": test_acc, "loss": test_eval_loss})

            is_best = False
            if acc > self.best_metric:
                is_best = True
                self.best_metric = acc
                self.best_epoch = epoch_idx
                self.no_climbing_cnt = 0
            else:
                self.no_climbing_cnt += 1

            if is_best and self.config.save_best_ckpt:
                self.save_ckpt("best", epoch_idx)
                self.categorical_score(all_answer, f"epoch{epoch_idx}_score.json")
                self.categorical_score(
                    test_all_answer, f"epoch{epoch_idx}_test_score.json"
                )
                dump_json(
                    test_all_answer,
                    os.path.join(
                        self.config.score_dir, f"epoch{epoch_idx}_all_test_answer.json"
                    ),
                    indent=4,
                )

            logger.info(
                (
                    f"Epoch: {epoch_idx}, train_loss: {train_loss:.3f}, eval_loss: {eval_loss:.3f},  dev: ACC: {acc:.4f}"
                    f"Epoch: {epoch_idx}, is_best: {is_best}, Dev: {acc}, Test: {test_acc}"
                )
            )

            if (
                self.config.num_early_stop > 0
                and self.no_climbing_cnt > self.config.num_early_stop
            ):
                break

        logger.info(
            (
                f"Trial finished. Best Epoch: {self.best_epoch}, Dev: {self.history['dev'][self.best_epoch]}, "
                f"Best Test: {self.history['test'][self.best_epoch]}"
            )
        )

    @torch.no_grad()
    def eval(self, dataset_name):
        """使用dev set/test set评价"""
        correct_num, all_num = 0, 0
        all_answer = []
        self.model.eval()
        name2loader = {
            "train": self.data_manager.train_loader,
            "dev": self.data_manager.dev_loader,
            "test": self.data_manager.test_loader,
        }
        loader = tqdm(name2loader[dataset_name], desc=f"{dataset_name} Eval")

        eval_num = 0
        total_loss = 0
        for batch in loader:
            batch = move_to_device(batch, self.config.device)
            raw_data = batch.pop("raw_data")
            return_obj = self.model(**batch)
            logits = return_obj["logits"].detach().cpu()
            preds = return_obj["preds"].detach().cpu().tolist()
            loss = return_obj["loss"]

            total_loss += loss.item() * logits.shape[0]
            eval_num += logits.shape[0]

            label_list = batch["label"]

            for i in range(logits.shape[0]):
                pred_tag = preds[i]
                gold_tag = int(label_list[i].item())

                all_num += 1

                if pred_tag == gold_tag:
                    correct_num += 1

                one_answer = raw_data[i]
                one_answer["pred_tag"] = pred_tag
                one_answer["gold_tag"] = gold_tag
                all_answer.append(one_answer)

        eval_loss = total_loss / eval_num
        ACC = correct_num / all_num

        return ACC, eval_loss, all_answer

    def categorical_score(self, all_answer: List[dict], write_file: str):
        """按数据类型计算分类ACC"""
        score_dict = {}
        for one_answer in tqdm(all_answer):
            data_type = one_answer["type"]
            if data_type not in score_dict:
                score_dict[data_type] = {"correct_num": 0, "all_num": 0}

            # accurucy
            score_dict[data_type]["all_num"] += 1  # 数据总量
            if one_answer["gold_tag"] == one_answer["pred_tag"]:
                score_dict[data_type]["correct_num"] += 1

        all_num, all_correct_num = 0, 0
        for data_type, score_item in score_dict.items():

            all_num += score_item["all_num"]
            all_correct_num += score_item["correct_num"]

            acc = score_item["correct_num"] / score_item["all_num"]

            score_item["ACC"] = round(acc, 4)

        score_dict["all"] = {}
        score_dict["all"]["ACC"] = round(all_correct_num / all_num, 4)

        dump_json(
            score_dict,
            os.path.join(self.config.score_dir, write_file),
            indent=4,
        )

    @torch.no_grad()
    def predict(self, sentence1: str, sentence2: str) -> int:
        """
        Args:
            sentence1: the first sentence
            sentence2: the second sentence

        Returns:
            the predicted value, `1` means the two sentences should
                be concatenated, otherwise should not
        """
        self.model.eval()
        concat_result = self.predict_batch(
            [{"sentence1": sentence1, "sentence2": sentence2}]
        )
        return concat_result[0]["pred_tag"]

    @torch.no_grad()
    def predict_batch(self, json_objs: List[dict]) -> List[dict]:
        for obj in json_objs:
            obj.update({"label": -1})

        self.model.eval()
        all_answer = []
        all_data = self.transform.predict_transform(json_objs)
        batch_list = [
            all_data[i : i + self.config.eval_batch_size]
            for i in range(0, len(all_data), self.config.eval_batch_size)
        ]

        for batch in batch_list:
            tensor_batch = self.data_manager.collate_fn(batch)
            tensor_batch = move_to_device(tensor_batch, self.config.device)
            raw_data = tensor_batch.pop("raw_data")

            return_obj = self.model(**tensor_batch)
            logits = return_obj["logits"]
            preds = return_obj["preds"]

            for i in range(logits.shape[0]):
                one_answer = raw_data[i]
                one_answer["pred_tag"] = preds[i].item()
                all_answer.append(one_answer)

        return all_answer
