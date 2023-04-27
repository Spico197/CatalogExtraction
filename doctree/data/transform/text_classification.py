from typing import Iterable, Optional, List

import torch
from rex.utils.logging import logger
from rex.utils.progress_bar import tqdm
from rex.data.label_encoder import LabelEncoder
from rex.data.transforms.base import TransformBase
from transformers import BertTokenizerFast


def text_classification_collate_fn(data):
    final_data = {
        "text": [],
        "input_ids": [],
        "attention_mask": [],
        "token_type_ids": [],
        "labels": [],
    }
    for d in data:
        for key in final_data:
            if key in d:
                final_data[key].append(d[key])

    final_data["input_ids"] = torch.tensor(final_data["input_ids"], dtype=torch.long)
    final_data["attention_mask"] = torch.tensor(
        final_data["attention_mask"], dtype=torch.long
    )
    final_data["token_type_ids"] = torch.tensor(
        final_data["token_type_ids"], dtype=torch.long
    )
    if len(final_data["labels"]) > 0:
        final_data["labels"] = torch.tensor(final_data["labels"], dtype=torch.long)
    else:
        final_data["labels"] = None
    return final_data


class TextClassificationTransform(TransformBase):
    """Cached data transform for classification task."""

    def __init__(self, tokenizer: BertTokenizerFast, max_seq_len: int) -> None:
        super().__init__(max_seq_len)

        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len

        self.label_encoder = LabelEncoder()

    def tokenize(self, text: str) -> dict:
        tokenized = self.tokenizer.encode_plus(
            text=text,
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
        dataset: Iterable,
        desc: Optional[str] = "Transform",
        debug: Optional[bool] = False,
        **kwargs,
    ) -> List[dict]:
        final_data = []
        if debug:
            dataset = dataset[:500]
        transform_loader = tqdm(dataset, desc=desc)

        num_tot_ins = 0
        for data in transform_loader:
            for sent in data["sents"]:
                label = sent["label"]
                label_id = self.label_encoder.update_encode_one(label)
                text = sent["text"]
                tokenized = self.tokenize(text)
                input_ids = tokenized["input_ids"]
                attention_mask = tokenized["attention_mask"]
                token_type_ids = tokenized["token_type_ids"]

                ins = {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask,
                    "token_type_ids": token_type_ids,
                    "labels": label_id,
                    "text": text,
                }
                final_data.append(ins)
                num_tot_ins += 1

        logger.info(transform_loader)
        logger.info(f"#Total Ins: {num_tot_ins}")

        return final_data

    def predict_transform(self, data: dict):
        """
        Args:
            data:
                {
                    "text": "text",
                }
        """
        text = data["text"]
        tokenized = self.tokenize(text)
        input_ids = tokenized["input_ids"]
        attention_mask = tokenized["attention_mask"]
        token_type_ids = tokenized["token_type_ids"]

        obj = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
            "text": text,
        }
        return obj
