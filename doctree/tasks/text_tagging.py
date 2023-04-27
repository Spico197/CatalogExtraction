import json
import time
from pathlib import Path
from collections import defaultdict

from omegaconf import OmegaConf
import torch
import torch.optim as optim
from rex.utils.config import ConfigParser
from rex.utils.logging import logger
from rex.utils.io import dump_json, load_line_json
from rex.utils.io import load_line_json, load_line_json_iterator
from rex.data.dataset import CachedDataset
from rex.data.manager import CachedManager
from rex.utils.tensor_move import move_to_cuda_device
from rex.utils.progress_bar import tqdm
from rex.tasks.base_task import TaskBase
from rex.utils.initialization import init_all
from rex.utils.tensor_move import move_to_device
from rex.utils.tagging import get_entities_from_tag_seq
from rex.metrics.tagging import tagging_prf1
from rex.metrics import calc_p_r_f1_from_tp_fp_fn

from doctree.data.transform.text_tagging import (
    HeadingTaggingTransform,
    tagging_collate_fn,
)
from doctree.data.definition import Node, NodeType
from doctree.data.convert import line_reorder
from doctree.models.text_tagging import LSTMCRFModel
from transformers import BertTokenizerFast
from doctree.data.convert import convert_tagging_text_to_node


class TextTaggingTask(TaskBase):
    def __init__(self, config):
        super().__init__(config)
        self.middle_path = Path(config.task_dir).joinpath("middle")
        self.middle_path.mkdir(parents=True, exist_ok=True)
        self.tokenizer = BertTokenizerFast.from_pretrained(config.plm_dir)
        self.transform = HeadingTaggingTransform(
            self.tokenizer, config.max_seq_len, config.num_sents
        )
        self.data_manager = CachedManager(
            config.train_filepath,
            config.dev_filepath,
            config.test_filepath,
            CachedDataset,
            self.transform,
            load_line_json,
            config.train_batch_size,
            config.eval_batch_size,
            tagging_collate_fn,
            debug_mode=config.debug_mode,
            load_train_data=not config.skip_train,
            load_dev_data=not config.skip_train,
            load_test_data=not config.skip_final_eval,
        )

        self.model = LSTMCRFModel(
            config,
            config.plm_dir,
            config.emb_size,
            config.hidden_size,
            num_lstm_layers=config.num_lstm_layers,
            num_tags=self.transform.label_encoder.num_tags,
            dropout=config.dropout,
        )
        self.model = self.model.to(self.config.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=config.learning_rate)

    @torch.no_grad()
    def eval(self, dataset_name, verbose=False, postfix=""):
        self.model.eval()
        name2loader = {
            "train": self.data_manager.train_eval_loader,
            "dev": self.data_manager.dev_loader,
            "test": self.data_manager.test_loader,
        }
        loader = tqdm(
            name2loader[dataset_name], desc=f"{dataset_name} Eval", ncols=80, ascii=True
        )

        hierarchical_measure = self.hierarchical_eval(dataset_name)
        measures = {
            "hierarchy":hierarchical_measure
        }

        return measures

    @torch.no_grad()
    def predict(self, article: dict):
        self.model.eval()
        batch = self.transform.predict_transform(article)
        tensor_batch = self.data_manager.collate_fn([batch])
        tensor_batch = move_to_device(tensor_batch, self.config.device)
        outs = self.model(**tensor_batch)
        pred_tag = outs["preds"][0]
        pred_tag = self.transform.label_encoder.decode(pred_tag)
        # text_labels = [{"text": [article["main_title"]], "label": "main_title"}]
        text_labels = []
        temp = []
        for idx in range(len(article["sents"])):
            if pred_tag[idx][0] == "B":
                temp.append(article["sents"][idx])
                if idx+1<len(article["sents"]) and \
                    (pred_tag[idx+1][0] == "B" or \
                    pred_tag[idx+1][0]== "O" or \
                    pred_tag[idx+1][2:] != pred_tag[idx][2:]):

                    text_labels.append({"text":temp, "label":pred_tag[idx][2:]})
                    temp = []
                elif idx+1 >= len(article["sents"]):
                    text_labels.append({"text":temp, "label":pred_tag[idx][2:]})
                    temp = []
            elif pred_tag[idx][0] == "I":
                temp.append(article["sents"][idx])
                if idx+1<len(article["sents"]) and \
                    (pred_tag[idx+1][0] == "B" or \
                    pred_tag[idx+1][0]== "O" or \
                    pred_tag[idx+1][2:] != pred_tag[idx][2:]):

                    text_labels.append({"text":temp, "label":pred_tag[idx][2:]})
                    temp = []
                elif idx+1 >= len(article["sents"]):
                    text_labels.append({"text":temp, "label":pred_tag[idx][2:]})
                    temp = []
            else:
                text_labels.append({"text":[article["sents"][idx]], "label":"text"})

        root_node = convert_tagging_text_to_node(text_labels)
        return root_node

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
            for batch in loader:
                batch = move_to_cuda_device(batch, self.config.device)
                result = self.model(**batch)
                loss = result["loss"]
                loader.set_postfix({"loss": loss.item()})
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            logger.info(loader)

            dev_measures = self.eval("dev")
            self.history["dev"].append(dev_measures)
            test_measures = self.eval("test")
            self.history["test"].append(test_measures)

            dev_select_measure = dev_measures["hierarchy"]["overall"]["f1"]
            is_best = False

            if dev_select_measure > self.best_metric:
                is_best = True
                self.best_metric = dev_select_measure
                self.best_epoch = epoch_idx
                self.no_climbing_cnt = 0
            else:
                self.no_climbing_cnt += 1

            if is_best and self.config.save_best_ckpt:
                self.save_ckpt(f"{epoch_idx}.{100 * dev_select_measure:.3f}", epoch_idx)
                self.save_ckpt("best", epoch_idx)
            test_measures_f1 = test_measures["hierarchy"]["overall"]["f1"]
            logger.info(
                (
                    f"Epoch: {epoch_idx}, is_best: {is_best}, "
                    f"Dev: {100 * dev_select_measure:.3f}, "
                    f"Test: {100 * test_measures_f1:.3f}"
                )
            )

            if (
                self.config.num_early_stop > 0
                and self.no_climbing_cnt > self.config.num_early_stop
            ):
                break

        logger.info("Trial finished.")
        self.print_final_record()
    
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
                if len(data["sents"]) < 1:
                    continue
                golds.append(data["tree_data"])
                tot += 1
                article = {
                    # "main_title":data["main_title"],
                    "sents":[]
                    }
                for sent in data["sents"]:
                    article["sents"].append(sent["text"])
         
                tot_num_unit += len(article["sents"]) + 1
                stime = time.time()
                pred_node = self.predict(article)
                utime = time.time() - stime
                tot_time += utime
                pred_json = pred_node.traverse()
                preds.append(pred_json)
                gold_data = data["tree_data"]
                if gold_data == pred_json:
                    correct += 1
                else:
                    fout_pred.write(
                        f"{json.dumps(pred_json, ensure_ascii=False, indent=2)}\n\n"
                    )
                    fout_answer.write(
                        f"{json.dumps(gold_data, ensure_ascii=False, indent=2)}\n\n"
                    )

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
        pred_nodes = set()
        gold_nodes = set()

        final_metrics = {}
        for pred, gold in zip(preds, golds):
            pred_level2heading = defaultdict(set)
            pred_level2text = defaultdict(set)
            gold_level2heading = defaultdict(set)
            gold_level2text = defaultdict(set)

            pred_node_list = line_reorder(pred)
            for node in pred_node_list:
                if node["label"] == NodeType.Root:
                    continue
                level = node["guid"].count(".")
                label = node["label"]
                pred_nodes.add((level, label, tuple(node["content"])))
                if label == NodeType.Heading:
                    pred_level2heading[level].add(tuple(node["content"]))
                else:
                    pred_level2text[level].add(tuple(node["content"]))

            gold_node_list = line_reorder(gold)
            for node in gold_node_list:
                if node["label"] == NodeType.Root:
                    continue
                level = node["guid"].count(".")
                label = node["label"]
                gold_nodes.add((level, label, tuple(node["content"])))
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

        for hlevel in nlevel_hresult:
            final_metrics[f"h{hlevel}"] = calc_p_r_f1_from_tp_fp_fn(
                nlevel_hresult[hlevel]["tp"],
                nlevel_hresult[hlevel]["fp"],
                nlevel_hresult[hlevel]["fn"],
            )
        for tlevel in nlevel_tresult:
            final_metrics[f"t{tlevel}"] = calc_p_r_f1_from_tp_fp_fn(
                nlevel_tresult[hlevel]["tp"],
                nlevel_tresult[hlevel]["fp"],
                nlevel_tresult[hlevel]["fn"],
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
