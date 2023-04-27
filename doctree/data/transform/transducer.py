import math
from copy import deepcopy as dcopy
from typing import Iterable, List, Optional, Any, Iterator

import torch
from torch.utils.data import IterableDataset
from transformers.file_utils import PaddingStrategy
from transformers.models.bert.tokenization_bert_fast import BertTokenizerFast
from rex.data.transforms.base import TransformBase
from rex.data.label_encoder import LabelEncoder
from rex.utils.progress_bar import tqdm
from transformers.tokenization_utils_base import TruncationStrategy

from doctree.data.convert import convert_json_to_node
from doctree.data.definition import Action, Node, NodeType, ShiftReduceAction
from doctree.utils.guid import parse_guid


def transducer_collate_fn(data: list):
    final_data = {
        "heading": {"input_ids": [], "token_type_ids": [], "attention_mask": []},
        "total": {"input_ids": [], "token_type_ids": [], "attention_mask": []},
        "buffer": {"input_ids": [], "token_type_ids": [], "attention_mask": []},
        "action": [],
    }
    for d in data:
        for x1 in ["heading", "total", "buffer"]:
            for x2 in ["input_ids", "token_type_ids", "attention_mask"]:
                final_data[x1][x2].append(d[x1][x2])
        for x1 in ["action"]:
            final_data[x1].append(d[x1])
    for x1 in ["heading", "total", "buffer"]:
        for x2 in ["input_ids", "token_type_ids", "attention_mask"]:
            final_data[x1][x2] = torch.tensor(final_data[x1][x2])
    final_data["action"] = torch.tensor(final_data["action"])
    return final_data


class TransducerStreamReadDataset(IterableDataset):
    def __init__(
        self,
        data_iterator: Iterator,
        transform,
        debug: Optional[bool] = False,
        num_docs: Optional[int] = -1,
    ) -> None:
        super().__init__()

        self.transform = transform
        self.data_iterator = data_iterator
        self.debug = debug
        self.num_docs = num_docs
        self.cnt_docs = 0
        self.cnt = 0

    def __iter__(self):
        for item in self.data_iterator:
            if self.num_docs > 0 and self.cnt_docs >= self.num_docs:
                break
            if self.debug and self.cnt >= 500:
                break
            for one in self.transform(item):
                yield one
                self.cnt += 1
            self.cnt_docs += 1


class TransducerTransform(TransformBase):
    def __init__(
        self,
        tokenizer: BertTokenizerFast,
        max_seq_len: int,
        truncation_strategy: Optional[str] = "end",
        use_stream_transform: Optional[bool] = False,
    ) -> None:
        super().__init__(max_seq_len)
        self.vocab = None
        self.action2label = LabelEncoder(
            {"Concat": 0, "SubHeading": 1, "SubText": 2, "Reduce": 3}
        )
        self.tokenizer = dcopy(tokenizer)
        self.truncation_strategy = truncation_strategy
        self.use_stream_transform = use_stream_transform

        if self.use_stream_transform:
            self.transform = self.stream_transform
        else:
            self.transform = self.cache_transform

    def stream_transform(self, json_obj: dict):
        transformed: List[dict] = self.construct_one(json_obj)
        return transformed

    def cache_transform(
        self,
        lines: Iterable[str],
        debug: Optional[bool] = False,
        num_docs: Optional[int] = -1,
    ):
        whole_data = []
        for idx, line in enumerate(tqdm(lines)):
            if num_docs > 0 and idx >= num_docs:
                break
            if debug and idx > 7:
                break
            one_data = self.construct_one(line)
            whole_data.extend(one_data)
        return whole_data

    def tokenize(self, string: str):
        result = {"string": string}
        if self.truncation_strategy == "start":
            string = string[-self.max_seq_len :]
        elif self.truncation_strategy == "end":
            string = string[: self.max_seq_len]
        elif self.truncation_strategy == "middle":
            len_overflow = len(string) - self.max_seq_len
            if len_overflow > 0:
                slice1 = string[: (len(string) - len_overflow) // 2]
                len_slice2 = self.max_seq_len - len(slice1)
                slice2 = string[-len_slice2:]
                string = slice1 + slice2
        elif self.truncation_strategy == "both_ends":
            len_overflow = len(string) - self.max_seq_len
            if len_overflow > 0:
                half_len_overflow = len_overflow // 2
                string = string[
                    half_len_overflow : half_len_overflow + self.max_seq_len
                ]
        else:
            raise ValueError(
                f"truncation_strategy: {self.truncation_strategy} is not supported"
            )

        results = self.tokenizer.encode_plus(
            string,
            truncation=TruncationStrategy.LONGEST_FIRST,
            padding=PaddingStrategy.MAX_LENGTH,
            max_length=self.max_seq_len,
            return_attention_mask=True,
            return_token_type_ids=True,
        )
        result.update(results)
        return result

    def _index(self, lst: list, obj: Any) -> int:
        for idx, iobj in enumerate(lst):
            if iobj is obj:
                return idx
        return -1

    def construct_one(self, json_obj: dict) -> Iterable:
        one_data = []
        node_list = []
        root_node = convert_json_to_node(json_obj)

        def traverse(node: Node):
            """only collect leaf nodes"""
            if node is None:
                return

            # concat action
            if len(node.content) > 1:
                for i in range(1, len(node.content)):
                    h_top = self.tokenize("".join(node.parent.content))
                    t_top = self.tokenize(node.content[i - 1])
                    b_input = self.tokenize(node.content[i])
                    action = self.action2label.update_encode_one(Action.Concat)

                    one_data.append(
                        {
                            "heading": h_top,
                            "total": t_top,
                            "buffer": b_input,
                            "action": action,
                        }
                    )
            if len(node_list) > 0:
                # if node.label != NodeType.Root:
                parent_guid = parse_guid(node.parent.guid)
                curr_node_idx = self._index(node.parent.children, node)
                last_node = node_list[-1]
                # if curr_node_idx > 0:
                #     last_node = node.parent.children[curr_node_idx - 1]
                # else:
                #     last_node = node.parent
                last_guid = parse_guid(last_node.guid)
                current_guid = parse_guid(node.guid)

                if last_node.parent is None:
                    # last node is Root, current node is the title
                    h_top = self.tokenize("".join(last_node.content))
                else:
                    h_top = self.tokenize("".join(last_node.parent.content))
                t_top = self.tokenize("".join(last_node.content))
                # only the first one is considered as sub
                b_input = self.tokenize(node.content[0])
                # sub
                if len(current_guid) > len(last_guid):
                    if node.label == NodeType.Heading:
                        action = self.action2label.update_encode_one(Action.SubHeading)
                    elif node.label == NodeType.Text:
                        action = self.action2label.update_encode_one(Action.SubText)
                    else:
                        raise ValueError(f"Check node label: {node.label}")
                    one_data.append(
                        {
                            "heading": h_top,
                            "total": t_top,
                            "buffer": b_input,
                            "action": action,
                        }
                    )
                else:
                    # reduce
                    while len(current_guid) <= len(last_guid):
                        h_top = self.tokenize("".join(last_node.parent.content))
                        t_top = self.tokenize("".join(last_node.content))
                        action = self.action2label.update_encode_one(Action.Reduce)
                        one_data.append(
                            {
                                "heading": h_top,
                                "total": t_top,
                                "buffer": b_input,
                                "action": action,
                            }
                        )
                        last_node = last_node.parent
                        last_guid = parse_guid(last_node.guid)

                    assert len(last_guid) > 0
                    h_top = self.tokenize("".join(last_node.parent.content))
                    t_top = self.tokenize("".join(last_node.content))
                    if node.label == NodeType.Heading:
                        action = self.action2label.update_encode_one(Action.SubHeading)
                    elif node.label == NodeType.Text:
                        action = self.action2label.update_encode_one(Action.SubText)
                    else:
                        raise ValueError(f"Check node label: {node.label}")
                    one_data.append(
                        {
                            "heading": h_top,
                            "total": t_top,
                            "buffer": b_input,
                            "action": action,
                        }
                    )

            node_list.append(node)
            if len(node.children) > 0:
                for child in node.children:
                    traverse(child)

        traverse(root_node)
        return one_data

    def predict_transform(
        self, total_stack_content: List[str], input_buffer_content: List[str]
    ):
        whole_data = {"heading": [], "total": [], "buffer": [], "action": 0}
        s_str = "".join(total_stack_content)
        total_stack_top = self.tokenize(s_str)
        whole_data["heading"] = total_stack_top
        whole_data["total"] = total_stack_top

        e_str = "".join(input_buffer_content)
        input_buffer = self.tokenize(e_str)
        whole_data["buffer"] = input_buffer

        return whole_data


def heading_cls_collate_fn(data: list):
    final_data = {
        "input_ids": [],
        "token_type_ids": [],
        "attention_mask": [],
        "labels": [],
    }
    for d in data:
        final_data["input_ids"].append(d["input_ids"])
        final_data["token_type_ids"].append(d["token_type_ids"])
        final_data["attention_mask"].append(d["attention_mask"])
        final_data["labels"].append(d["label"])
    for x2 in ["input_ids", "token_type_ids", "attention_mask", "labels"]:
        final_data[x2] = torch.tensor(final_data[x2])
    return final_data


class HeadingClsTransform(TransducerTransform):
    def __init__(self, tokenizer: BertTokenizerFast, max_seq_len: int) -> None:
        super().__init__(tokenizer, max_seq_len)

    def construct_one(self, json_obj: dict) -> Iterable:
        one_data = []
        root_node = convert_json_to_node(json_obj)

        def traverse(node: Node):
            """only collect leaf nodes"""
            if node is None:
                return

            if len(node.content) > 0:
                b_input = self.tokenize("".join(node.content))
                node_label = self.action2label.update_encode_one(node.label)
                b_input.update({"label": node_label})
                one_data.append(b_input)

            if len(node.children) > 0:
                for child in node.children:
                    traverse(child)

        traverse(root_node)
        return one_data
