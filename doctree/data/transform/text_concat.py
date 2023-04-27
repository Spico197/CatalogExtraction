from typing import Iterable, Optional, List

import torch
from transformers import BertTokenizerFast
from rex.data.transforms.base import TransformBase
from rex.utils.progress_bar import tqdm


def text_concat_collate_fn(data: list):
    final_data = {
        "raw_data": [],
        "input_ids": [],
        "token_type_ids": [],
        "attention_mask": [],
        "label": [],
    }
    for d in data:
        final_data["raw_data"].append(d["raw_data"])
        final_data["input_ids"].append(d["input_ids"])
        final_data["token_type_ids"].append(d["token_type_ids"])
        final_data["attention_mask"].append(d["attention_mask"])
        final_data["label"].append(d["label"])
    for x2 in ["input_ids", "token_type_ids", "attention_mask", "label"]:
        final_data[x2] = torch.tensor(final_data[x2])
    return final_data


class TextConcatTransform(TransformBase):
    def __init__(self, tokenizer: BertTokenizerFast, max_seq_len: int) -> None:
        super().__init__(max_seq_len)

        self.tokenizer = tokenizer
        self.vocab = None

    def tokenize(self, text1: str, text2: str) -> dict:
        tokenized = self.tokenizer.encode_plus(
            text=text1,
            text_pair=text2,
            add_special_tokens=True,
            padding="max_length",
            max_length=self.max_seq_len,
            truncation=True,
            return_attention_mask=True,
            return_token_type_ids=True,
        )
        return tokenized

    def transform(
        self,
        lines: Iterable,
        proportion: Optional[float] = 1.0,
        debug: Optional[bool] = False,
    ):
        load_data = None
        # 测试训练集需要多少数据即可达到目标效果
        data_size = len(lines)
        load_size = int(data_size * proportion)
        load_data = lines[:load_size]

        whole_data = []
        for idx, d in enumerate(tqdm(load_data, desc="Transform")):
            if debug and idx > 127:
                break
            one_data = self.construct_one(d)
            if one_data["label"] is None:
                continue
            whole_data.append(one_data)
        return whole_data

    def construct_one(self, json_obj: dict):
        tokenized = self.tokenize(json_obj["sentence1"], json_obj["sentence2"])
        one = {
            "raw_data": json_obj,
            "input_ids": tokenized["input_ids"],
            "attention_mask": tokenized["attention_mask"],
            "token_type_ids": tokenized["token_type_ids"],
            "label": json_obj.get("label"),
        }
        return one

    def predict_transform(self, json_objs: List[dict]):
        all_data = []
        for data in json_objs:
            one = self.construct_one(data)
            all_data.append(one)
        return all_data
