import json
import time
import math
from pathlib import Path
from collections import defaultdict
from typing import List, Optional

import torch
from torch.optim import AdamW
from torch.nn import parallel
from torch.utils.tensorboard import SummaryWriter
from omegaconf import OmegaConf
from transformers import AutoTokenizer
from transformers.optimization import get_linear_schedule_with_warmup
from rex.utils.logging import logger
from rex.utils.io import load_line_json, load_line_json_iterator
from rex.utils.progress_bar import tqdm
from rex.utils.tensor_move import move_to_device
from rex.data.dataset import CachedDataset
from rex.tasks.base_task import TaskBase
from rex.metrics.classification import mc_prf1
from rex.utils.wrapper import safe_try
from rex.metrics import calc_p_r_f1_from_tp_fp_fn

from doctree.data.definition import Node, NodeType
from doctree.data.convert import line_reorder
from doctree.data.manager import StreamTransformManager, CachedManager
from doctree.data.transform import (
    TransducerTransform,
    transducer_collate_fn,
    TransducerStreamReadDataset,
)
from doctree.models.transducer import (
    TransducerWithBert,
)
from doctree.utils.doc_tree_decoding import decode_tree, decode_tree_with_constraint


class TransducerDocTreeConstructionTask(TaskBase):
    def __init__(self, config: OmegaConf, **kwargs) -> None:
        super().__init__(config, **kwargs)

        logger.debug("loading tokenizer")
        tokenizer = AutoTokenizer.from_pretrained(config.plm_dir)
        logger.debug("tokenizer loaded")
        logger.debug("initialise transformation")
        self.transform = TransducerTransform(
            tokenizer,
            config.max_seq_len,
            truncation_strategy=config.truncation_strategy,
            use_stream_transform=config.use_stream_data_iterator,
        )
        logger.debug("transformation initialised")

        logger.debug("preparing data manager")
        if config.use_stream_data_iterator:
            self.data_manager = StreamTransformManager(
                config.train_filepath,
                config.dev_filepath,
                config.test_filepath,
                TransducerStreamReadDataset,
                self.transform,
                load_line_json_iterator,
                config.train_batch_size,
                config.eval_batch_size,
                transducer_collate_fn,
                train_shuffle=False,
                eval_shuffle=False,
                debug_mode=config.debug_mode,
                train_docs=config.train_docs,
                load_train_data=config.load_train_data,
                load_dev_data=config.load_dev_data,
                load_test_data=config.load_test_data,
            )
        else:
            self.data_manager = CachedManager(
                config.train_filepath,
                config.dev_filepath,
                config.test_filepath,
                CachedDataset,
                self.transform,
                load_line_json,
                config.train_batch_size,
                config.eval_batch_size,
                transducer_collate_fn,
                debug_mode=config.debug_mode,
                train_docs=config.train_docs,
                load_train_data=config.load_train_data,
                load_dev_data=config.load_dev_data,
                load_test_data=config.load_test_data,
            )
        logger.debug("data manager OK")

        logger.debug("initialise model and optimiser")
        self.model = TransducerWithBert(
            config.plm_dir, self.transform.action2label.num_tags
        )
        self.model.to(self.config.device)
        self.optimizer = AdamW(self.model.parameters(), lr=config.learning_rate)
        self.writer = SummaryWriter(Path(config.task_dir).joinpath("summary"))
        # self.lr_scheduler = self.init_lr_scheduler()
        logger.debug("model and optimiser OK")

    # def init_lr_scheduler(self):
    #     # num_training_steps = 1983248
    #     num_training_steps = 4784 * self.config.num_epochs
    #     num_warmup_steps = math.floor(
    #         num_training_steps * self.config.warmup_proportion
    #     )
    #     return get_linear_schedule_with_warmup(
    #         self.optimizer,
    #         num_warmup_steps=num_warmup_steps,
    #         num_training_steps=num_training_steps,
    #     )

    @safe_try
    def train(self):
        num_steps = 0
        for epoch_idx in range(self.config.num_epochs):
            logger.info(f"Epoch: {epoch_idx}/{self.config.num_epochs}")
            self.model.train()
            loader = tqdm(self.data_manager.train_loader, desc=f"Train(e{epoch_idx})")
            for batch in loader:
                batch = move_to_device(batch, self.config.device)
                result = self.model(**batch)
                loss = result["loss"]
                loader.set_postfix({"loss": loss.item()})
                self.writer.add_scalar("loss/train", loss.item(), num_steps)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                # self.lr_scheduler.step()
                # if (num_steps + 1) % 10000 == 0:
                #     self.save_ckpt(f"step.{num_steps}")
                num_steps += 1
            logger.info(loader)

            dev_measures = self.eval("dev")
            self.history["dev"].append(dev_measures)
            test_measures = self.eval("test")
            self.history["test"].append(test_measures)

            is_best = False
            dev_select_measure = dev_measures["hierarchy"]["overall"]["f1"]
            # if dev_measures["macro"]["f1"] > self.best_metric:
            if dev_select_measure > self.best_metric:
                is_best = True
                self.best_metric = dev_select_measure
                self.best_epoch = epoch_idx
                self.no_climbing_cnt = 0
            else:
                self.no_climbing_cnt += 1

            if is_best and self.config.save_best_ckpt:
                self.save_ckpt("best", epoch_idx)

            logger.info(
                f"Epoch: {epoch_idx}, is_best: {is_best}, Dev: {dev_measures}, Test: {test_measures}"
            )

            if (
                self.config.num_early_stop > 0
                and self.no_climbing_cnt > self.config.num_early_stop
            ):
                break
        self.writer.close()
        logger.info(
            (
                f"Trial finished. Best Epoch: {self.best_epoch}, Dev: {self.history['dev'][self.best_epoch]}, "
                f"Best Test: {self.history['test'][self.best_epoch]}"
            )
        )

    @torch.no_grad()
    def eval(self, dataset_name):
        self.model.eval()
        name2loader = {
            "train": self.data_manager.train_loader,
            "dev": self.data_manager.dev_loader,
            "test": self.data_manager.test_loader,
        }
        loader = tqdm(name2loader[dataset_name], desc=f"{dataset_name} Eval")
        pred_actions = []
        gold_actions = []
        for batch in loader:
            batch = move_to_device(batch, self.config.device)
            gold_actions.extend(batch["action"].detach().cpu().tolist())
            del batch["action"]
            result = self.model(**batch)
            action_out = result["preds"]
            pred_actions.extend(action_out.detach().long().cpu().tolist())
        logger.info(loader)
        action_measures = mc_prf1(
            pred_actions,
            gold_actions,
            num_classes=self.transform.action2label.num_tags,
            label_idx2name=self.transform.action2label.id2label,
        )
        hierarchical_measures = self.hierarchical_eval(dataset_name)
        measures = {"action": action_measures, "hierarchy": hierarchical_measures}
        return measures

    @torch.no_grad()
    def predict_api_for_decoding(
        self, total_stack_content: List[str], input_buffer_content: List[str]
    ) -> str:
        self.model.eval()
        whole_data = self.transform.predict_transform(
            total_stack_content, input_buffer_content
        )
        final_data = self.data_manager.collate_fn([whole_data])
        del final_data["action"]
        batch = move_to_device(final_data, self.config.device)
        results = self.model(**batch)
        action = results["preds"][0].item()
        return self.transform.action2label.decode([action])[0]

    @torch.no_grad()
    def action2probs_predict_api(
        self, total_stack_content: List[str], input_buffer_content: List[str]
    ) -> str:
        self.model.eval()
        whole_data = self.transform.predict_transform(
            total_stack_content, input_buffer_content
        )
        final_data = self.data_manager.collate_fn([whole_data])
        batch = move_to_device(final_data, self.config.device)
        results = self.model(**batch)
        action2probs = {}
        probs = results["logits"][0].softmax(-1).detach().tolist()
        actions = self.transform.action2label.decode(list(range(len(probs))))
        for action, prob in zip(actions, probs):
            action2probs[action] = prob
        return action2probs

    @torch.no_grad()
    def predict(self, texts: List[str], with_constraint: Optional[bool] = True) -> Node:
        self.model.eval()
        if with_constraint:
            root_node = decode_tree_with_constraint(
                self.action2probs_predict_api, texts
            )
        else:
            root_node = decode_tree(self.predict_api_for_decoding, texts)
        return root_node

    def load_pretrained_model(self, path):
        logger.info("load pretrained model from {}".format(path))
        if torch.cuda.device_count() == 0:
            store_dict = torch.load(path, map_location="cpu")
        else:
            store_dict = torch.load(path, map_location=torch.device(self.config.device))

        if self.model and "model_state" in store_dict:
            if isinstance(self.model, parallel.DataParallel) or isinstance(
                self.model, parallel.DistributedDataParallel
            ):
                self.model.module.load_state_dict(store_dict["model_state"])
            else:
                self.model.load_state_dict(store_dict["model_state"])
            logger.info("Load model successfully")
        else:
            raise ValueError(
                f"Model loading failed. self.model={self.model}, stored_dict_keys={store_dict.keys()}"
            )

    @torch.no_grad()
    def hierarchical_eval(self, dataset_name):
        self.model.eval()
        name2filepath = {
            "train": self.config.train_filepath,
            "dev": self.config.dev_filepath,
            "test": self.config.test_filepath,
        }
        # eval on test
        fout_pred = (
            Path(self.config.task_dir)
            .joinpath(f"{dataset_name}_predict.json")
            .open("wt", encoding="utf8")
        )
        fout_answer = (
            Path(self.config.task_dir)
            .joinpath(f"{dataset_name}_answer.json")
            .open("wt", encoding="utf8")
        )

        tot = 0
        correct = 0
        tot_time = 0.0
        tot_num_unit = 0
        preds = []
        golds = []
        with Path(name2filepath[dataset_name]).open("rt", encoding="utf8") as fin:
            for line in tqdm(fin):
                data = json.loads(line)
                golds.append(data)
                tot += 1
                node_list = line_reorder(data)
                texts = []
                for node in node_list:
                    texts.extend(node["content"])
                tot_num_unit += len(texts) - 1
                # except the first ROOT
                stime = time.time()
                pred_node = self.predict(
                    texts[1:], with_constraint=self.config.with_constraint
                )
                utime = time.time() - stime
                tot_time += utime
                pred_json = pred_node.traverse()
                preds.append(pred_json)
                if data == pred_json:
                    correct += 1
                else:
                    fout_pred.write(
                        f"{json.dumps(pred_json, ensure_ascii=False, indent=2)}\n\n"
                    )
                    fout_answer.write(
                        f"{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
                    )
        logger.info(f"Overall Tree Acc: {100 * correct / (tot + 1e-12):.3f}%")
        logger.info(f"Avg. Number of Units per doc: {tot_num_unit / tot:.3f}")
        logger.info(
            f"Inference Time: {tot_time:.3f} s, {tot_time / tot:.3f} s/doc, {tot / tot_time:.3f} docs/s"
        )
        results = self.calc_hierarchical_metrics(preds, golds)
        logger.info(f"hierarchical_eval results: {results}")
        return results

    @torch.no_grad()
    def hierarchical_eval_on_path(self, filepath):
        self.model.eval()

        tot = 0
        correct = 0
        tot_time = 0.0
        tot_num_unit = 0
        preds = []
        golds = []
        with Path(filepath).open("rt", encoding="utf8") as fin:
            for line in tqdm(fin):
                data = json.loads(line)
                golds.append(data)
                tot += 1
                node_list = line_reorder(data)
                texts = []
                for node in node_list:
                    texts.extend(node["content"])
                tot_num_unit += len(texts) - 1
                # except the first ROOT
                stime = time.time()
                pred_node = self.predict(
                    texts[1:], with_constraint=self.config.with_constraint
                )
                utime = time.time() - stime
                tot_time += utime
                pred_json = pred_node.traverse()
                preds.append(pred_json)
                if data == pred_json:
                    correct += 1

        logger.info(f"Overall Tree Acc: {100 * correct / (tot + 1e-12):.3f}%")
        logger.info(f"Avg. Number of Units per doc: {tot_num_unit / tot:.3f}")
        logger.info(
            f"Inference Time: {tot_time:.3f} s, {tot_time / tot:.3f} s/doc, {tot / tot_time:.3f} docs/s"
        )
        results = self.calc_hierarchical_metrics(preds, golds)
        logger.info(f"hierarchical_eval results: {results}")
        return results

    @staticmethod
    def calc_hierarchical_metrics(preds, golds):
        heading_result = {"tp": 0, "fp": 0, "fn": 0}
        nlevel_hresult = defaultdict(lambda: defaultdict(lambda: 0))
        text_result = {"tp": 0, "fp": 0, "fn": 0}
        nlevel_tresult = defaultdict(lambda: defaultdict(lambda: 0))
        overall_result = {"tp": 0, "fp": 0, "fn": 0}
        nlevel_oresult = defaultdict(lambda: defaultdict(lambda: 0))
        pred_nodes = set()
        gold_nodes = set()

        final_metrics = {}
        for pred, gold in zip(preds, golds):
            pred_level2heading = defaultdict(set)
            pred_level2text = defaultdict(set)
            pred_level2overall = defaultdict(set)
            gold_level2heading = defaultdict(set)
            gold_level2text = defaultdict(set)
            gold_level2overall = defaultdict(set)

            pred_node_list = line_reorder(pred)
            for node in pred_node_list:
                if node["label"] == NodeType.Root:
                    continue
                level = node["guid"].count(".")
                label = str(node["label"])
                pred_nodes.add((level, label, tuple(node["content"])))
                pred_level2overall[level].add((label, tuple(node["content"])))
                if label == NodeType.Heading:
                    pred_level2heading[level].add(tuple(node["content"]))
                else:
                    pred_level2text[level].add(tuple(node["content"]))

            gold_node_list = line_reorder(gold)
            for node in gold_node_list:
                if node["label"] == NodeType.Root:
                    continue
                level = node["guid"].count(".")
                label = str(node["label"])
                gold_nodes.add((level, label, tuple(node["content"])))
                gold_level2overall[level].add((label, tuple(node["content"])))
                if label == NodeType.Heading:
                    gold_level2heading[level].add(tuple(node["content"]))
                else:
                    gold_level2text[level].add(tuple(node["content"]))

            heading_max_depth = max(
                [
                    1,
                    max([1, *pred_level2heading.keys()]),
                    max([1, *gold_level2heading.keys()]),
                ]
            )
            # root is not taken into account
            for i in range(1, heading_max_depth + 1):
                tp = len(pred_level2heading[i] & gold_level2heading[i])
                fp = len(pred_level2heading[i] - gold_level2heading[i])
                fn = len(gold_level2heading[i] - pred_level2heading[i])

                nlevel_hresult[i]["tp"] += tp
                nlevel_hresult[i]["fp"] += fp
                nlevel_hresult[i]["fn"] += fn

                heading_result["tp"] += tp
                heading_result["fp"] += fp
                heading_result["fn"] += fn

            text_max_depth = max(
                [
                    1,
                    max([1, *pred_level2text.keys()]),
                    max([1, *gold_level2text.keys()]),
                ]
            )
            # root is not taken into account
            for i in range(1, text_max_depth + 1):
                tp = len(pred_level2text[i] & gold_level2text[i])
                fp = len(pred_level2text[i] - gold_level2text[i])
                fn = len(gold_level2text[i] - pred_level2text[i])

                nlevel_tresult[i]["tp"] += tp
                nlevel_tresult[i]["fp"] += fp
                nlevel_tresult[i]["fn"] += fn

                text_result["tp"] += tp
                text_result["fp"] += fp
                text_result["fn"] += fn

            overall_max_depth = max(
                [
                    1,
                    max([1, *pred_level2overall.keys()]),
                    max([1, *gold_level2overall.keys()]),
                ]
            )
            # root is not taken into account
            for i in range(1, overall_max_depth + 1):
                tp = len(pred_level2overall[i] & gold_level2overall[i])
                fp = len(pred_level2overall[i] - gold_level2overall[i])
                fn = len(gold_level2overall[i] - pred_level2overall[i])

                nlevel_oresult[i]["tp"] += tp
                nlevel_oresult[i]["fp"] += fp
                nlevel_oresult[i]["fn"] += fn

        for hlevel in nlevel_hresult:
            final_metrics[f"h{hlevel}"] = calc_p_r_f1_from_tp_fp_fn(
                nlevel_hresult[hlevel]["tp"],
                nlevel_hresult[hlevel]["fp"],
                nlevel_hresult[hlevel]["fn"],
            )
        for tlevel in nlevel_tresult:
            final_metrics[f"t{tlevel}"] = calc_p_r_f1_from_tp_fp_fn(
                nlevel_tresult[tlevel]["tp"],
                nlevel_tresult[tlevel]["fp"],
                nlevel_tresult[tlevel]["fn"],
            )
        for olevel in nlevel_oresult:
            final_metrics[f"o{olevel}"] = calc_p_r_f1_from_tp_fp_fn(
                nlevel_oresult[olevel]["tp"],
                nlevel_oresult[olevel]["fp"],
                nlevel_oresult[olevel]["fn"],
            )

        final_metrics["heading"] = calc_p_r_f1_from_tp_fp_fn(
            heading_result["tp"], heading_result["fp"], heading_result["fn"]
        )
        final_metrics["text"] = calc_p_r_f1_from_tp_fp_fn(
            text_result["tp"], text_result["fp"], text_result["fn"]
        )

        overall_result["tp"] = len(pred_nodes & gold_nodes)
        overall_result["fp"] = len(pred_nodes - gold_nodes)
        overall_result["fn"] = len(gold_nodes - pred_nodes)
        final_metrics["overall"] = calc_p_r_f1_from_tp_fp_fn(
            overall_result["tp"], overall_result["fp"], overall_result["fn"]
        )

        return final_metrics
