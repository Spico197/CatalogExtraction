from typing import Iterable, Optional, List
import torch
from rex.utils.logging import logger
from rex.utils.progress_bar import tqdm
from rex.data.label_encoder import LabelEncoder
from rex.data.transforms.base import TransformBase
from transformers import BertTokenizerFast


def tagging_collate_fn(data):
    final_data = {
        "input_ids": [],
        "attention_mask": [],
        "token_type_ids": [],
        "labels": [],
        "sents_mask": [],
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
    if len(final_data["sents_mask"]) >= 1:
        final_data["sents_mask"] = torch.tensor(
            final_data["sents_mask"], dtype=torch.long
        ).bool()
    else:
        final_data["sents_mask"] = None

    if len(final_data["labels"]) >= 1:
        final_data["labels"] = torch.tensor(final_data["labels"], dtype=torch.long)
    else:
        final_data["labels"] = None

    return final_data


class HeadingTaggingTransform(TransformBase):
    """Cached data transform for classification task."""

    def __init__(
        self, tokenizer: BertTokenizerFast, max_seq_len: int, num_sents: int
    ) -> None:
        super().__init__(max_seq_len)
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.label_encoder = LabelEncoder()
        self.num_sents = num_sents

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
        """
        final_data = [
            {
                "doc_id": doc_id,
                "input_ids": num_sents x seq_len,
                "attention_mask": num_sents x seq_len,
                "token_type_ids": num_sents x seq_len,
                "labels": num_sents
                "sents_mask": num_sents
            }, {}, {} ...
        ]
        """
        padding_text = "This is a sentence only for padding"
        padding_tokenized = self.tokenize(padding_text)
        padding_label = "O"
        final_data = []
        if debug:
            dataset = dataset[:50]
        transform_loader = tqdm(dataset, desc=desc)

        num_tot_ins = 0

        for data in transform_loader:
            all_text = data["sents"]
            if len(all_text) < self.num_sents:
                input_ids = []
                attention_mask = []
                token_type_ids = []
                label_ids = []

                for per_text_label in all_text:
                    per_text = per_text_label["text"]
                    tokenized = self.tokenize(per_text)
                    input_ids.append(tokenized["input_ids"])
                    attention_mask.append(tokenized["attention_mask"])
                    token_type_ids.append(tokenized["token_type_ids"])
                    label = per_text_label["label"]
                    label_ids.append(self.label_encoder.update_encode_one(label))

                for _ in range(self.num_sents - len(all_text)):
                    input_ids.append(padding_tokenized["input_ids"])
                    attention_mask.append([1] + [0] * (self.max_seq_len - 1))
                    token_type_ids.append(padding_tokenized["token_type_ids"])
                    label_ids.append(
                        self.label_encoder.update_encode_one(padding_label)
                    )

                sents_mask = [1] * len(attention_mask)
                for i in range(len(attention_mask)):
                    if sum(attention_mask[i]) == 1:
                        sents_mask[i] = 0
                ins = {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask,
                    "token_type_ids": token_type_ids,
                    "labels": label_ids,
                    "sents_mask": sents_mask,
                }
                final_data.append(ins)
                num_tot_ins += 1
            else:
                for start_indx in range(len(all_text) - self.num_sents + 1):
                    input_ids = []
                    attention_mask = []
                    token_type_ids = []
                    label_ids = []
                    for per_text_label in all_text[
                        start_indx : start_indx + self.num_sents
                    ]:
                        per_text = per_text_label["text"]
                        tokenized = self.tokenize(per_text)
                        input_ids.append(tokenized["input_ids"])
                        attention_mask.append(tokenized["attention_mask"])
                        token_type_ids.append(tokenized["token_type_ids"])
                        label = per_text_label["label"]
                        label_ids.append(self.label_encoder.update_encode_one(label))
                    sents_mask = [1] * len(attention_mask)
                    ins = {
                        "input_ids": input_ids,
                        "attention_mask": attention_mask,
                        "token_type_ids": token_type_ids,
                        "labels": label_ids,
                        "sents_mask": sents_mask,
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
                    "doc_id" : 123
                    "sents":[text,text,text....]
                }
        """
        obj = {
            "input_ids": [],
            "attention_mask": [],
            "token_type_ids": [],
            "text": [],
        }
        text = data["sents"]
        for per_text in text:
            tokenized = self.tokenize(per_text)
            obj["input_ids"].append(tokenized["input_ids"])
            obj["attention_mask"].append(tokenized["attention_mask"])
            obj["token_type_ids"].append(tokenized["token_type_ids"])
            obj["text"].append(per_text)
        return obj
