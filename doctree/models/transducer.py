from typing import List, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel

from rex.modules.ffn import FFN


class TransducerWithBert(nn.Module):
    def __init__(self, bert_dir: str, num_classes: int):
        super().__init__()

        self.encoder = BertModel.from_pretrained(bert_dir)
        self.hidden_dim = self.encoder.config.hidden_size

        # self.heading_ffn = FFN(self.hidden_dim, self.hidden_dim)
        # self.total_ffn = FFN(self.hidden_dim, self.hidden_dim)
        # self.buffer_ffn = FFN(self.hidden_dim, self.hidden_dim)
        # self.gate_ffn = FFN(self.hidden_dim, 1, mid_dims=[self.hidden_dim // 2])

        self.classifier = FFN(
            2 * self.hidden_dim, num_classes, mid_dims=[self.hidden_dim // 3]
        )

    def encoding(self, hidden: dict):
        output = self.encoder(
            input_ids=hidden["input_ids"],
            attention_mask=hidden["attention_mask"],
            token_type_ids=hidden["token_type_ids"],
        )
        return output.pooler_output

    def attention(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor):
        alpha = torch.bmm(query, key.transpose(-1, -2)) / torch.sqrt(self.hidden_dim)
        probs = alpha.softmax(-1)
        outputs = probs.mm(value)
        return (probs, outputs)

    def forward(
        self,
        heading: dict,
        total: dict,
        buffer: dict,
        action: Optional[dict] = None,
    ):
        """
        Args:
            headings: heading stack
            total: total stack
            buffer: input buffer
            action: action labels
        """
        buffer_hidden = self.encoding(buffer)
        # buffer_hidden = self.buffer_ffn(buffer_hidden)

        # headings_hidden = self.encoding(heading)
        # (batch_size, hidden_size)
        # headings_hidden = self.heading_ffn(headings_hidden)
        # _, headings_hidden = self.attention(
        #     buffer_hidden, headings_hidden, headings_hidden
        # )

        total_hidden = self.encoding(total)
        # (batch_size, hidden_size)
        # total_hidden = self.total_ffn(total_hidden)
        # _, total_hidden = self.attention(buffer_hidden, total_hidden, total_hidden)

        # gated_weight = torch.sigmoid(self.gate_ffn(buffer_hidden + headings_hidden))
        # comp_hidden = gated_weight * headings_hidden + (1 - gated_weight) * total_hidden
        # comp_hidden = torch.cat([buffer_hidden, comp_hidden], -1)
        # action_logits = self.classifier(comp_hidden)

        # comp_hidden = torch.cat([headings_hidden, buffer_hidden], dim=-1)
        # comp_hidden = torch.cat([buffer_hidden - headings_hidden, buffer_hidden - total_hidden], dim=-1)
        comp_hidden = torch.cat([total_hidden, buffer_hidden], dim=-1)
        action_logits = self.classifier(comp_hidden)

        return_obj = {"logits": action_logits, "preds": action_logits.argmax(-1)}
        if action is not None:
            loss = F.cross_entropy(action_logits, action)
            return_obj.update({"loss": loss})
        return return_obj


class HeadingClsWithBert(nn.Module):
    def __init__(self, bert_dir: str, num_classes: int):
        super().__init__()

        self.encoder = BertModel.from_pretrained(bert_dir)
        self.hidden_dim = self.encoder.config.hidden_size

        self.classifier = FFN(
            self.hidden_dim, num_classes, mid_dims=[self.hidden_dim // 3]
        )

    def encoding(self, input_ids, token_type_ids, attention_mask):
        output = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )
        return output.pooler_output

    def forward(
        self,
        input_ids: torch.Tensor,
        token_type_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        labels: Optional[dict] = None,
    ):
        hidden = self.encoding(input_ids, token_type_ids, attention_mask)
        label_logits = self.classifier(hidden)

        return_obj = {"logits": label_logits, "preds": label_logits.argmax(-1)}
        if labels is not None:
            loss = F.cross_entropy(label_logits, labels)
            return_obj.update({"loss": loss})
        return return_obj

    def predict_one(
        self,
        headings: List[torch.Tensor],
        total: List[torch.Tensor],
        buffer: List[torch.Tensor],
    ):
        pass
