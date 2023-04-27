from typing import Optional

import torch
import torch.nn as nn
from torch.nn import init
from transformers import BertModel
from rex.modules.ffn import FFN


class TextConcat(nn.Module):
    def __init__(
        self,
        plm_dir: str,
        pred_threshold: Optional[float] = 0.5,
        dropout: Optional[float] = 0.5,
    ) -> None:
        super().__init__()

        self.pred_threshold = pred_threshold
        self.bert_encoder = BertModel.from_pretrained(plm_dir)
        bert_dim = self.bert_encoder.config.hidden_size

        # 两层线性层，将维度从bert_dim降到1
        self.classifier = FFN(bert_dim, 1, (100,), dropout=dropout, act_fn=nn.Tanh())
        self.criterion = nn.BCEWithLogitsLoss(reduction="mean")

        self.reset_parameters()

    def reset_parameters(self):
        # 初始化线性层
        init.xavier_uniform_(self.classifier.ffn[0].weight)
        init.xavier_uniform_(self.classifier.ffn[3].weight)

    def get_encoded_text(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: torch.Tensor,
    ) -> torch.Tensor:
        bert_out = self.bert_encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )

        return bert_out.pooler_output

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: torch.Tensor,
        label: Optional[torch.Tensor] = None,
    ) -> dict:
        cls_out = self.get_encoded_text(input_ids, attention_mask, token_type_ids)
        logits = self.classifier(cls_out)
        logits = logits.squeeze(-1)

        return_obj = {
            "logits": logits.sigmoid(),
            "preds": logits.sigmoid().gt(self.pred_threshold).long(),
        }

        if label is not None:
            loss = self.criterion(logits, label.float())
            return_obj.update({"loss": loss})
        return return_obj
