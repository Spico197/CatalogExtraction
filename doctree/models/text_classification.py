from typing import Optional

import torch.nn as nn
from rex.modules.cnn import MultiKernelCNN
from rex.modules.ffn import FFN
from transformers import BertModel


class TextClassificationModel(nn.Module):
    def __init__(
        self,
        plm_filepath: str,
        num_filters: Optional[int] = 300,
        num_classes: Optional[int] = 3,
        dropout: Optional[float] = 0.5,
        kernel_sizes=[1, 3, 5],
        mid_dims=[
            100,
        ],
    ):
        super().__init__()

        self.plm = BertModel.from_pretrained(plm_filepath)
        hidden_size = self.plm.config.hidden_size
        self.cnn = MultiKernelCNN(
            in_channel=hidden_size,
            num_filters=num_filters,
            kernel_sizes=kernel_sizes,
            dropout=dropout,
        )

        self.ffn = FFN(
            input_dim=num_filters * len(kernel_sizes),
            output_dim=num_classes,
            mid_dims=mid_dims,
            dropout=dropout,
            act_fn=nn.LeakyReLU(),
        )

        self.loss = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None, **kwargs):
        plm_outs = self.plm(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            return_dict=True,
        )
        hidden = self.cnn(plm_outs.last_hidden_state)

        outs = self.ffn(hidden)

        probs, preds = outs.softmax(-1).max(-1)
        results = {"logits": outs, "probs": probs, "preds": preds}
        if labels is not None:
            results["loss"] = self.loss(outs, labels)
        return results
