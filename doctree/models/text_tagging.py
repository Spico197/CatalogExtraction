import torch
import torch.nn as nn
from rex.modules.crf import PlainCRF
from transformers import BertModel


class LSTMCRFModel(nn.Module):
    def __init__(
        self,
        config,
        plm_filepath: str,
        emb_size,
        hidden_size,
        num_lstm_layers,
        num_tags,
        dropout,
    ):
        super().__init__()
        self.config = config
        self.plm = BertModel.from_pretrained(plm_filepath)
        self.lstm_enc = nn.LSTM(
            emb_size,
            hidden_size,
            num_layers=num_lstm_layers,
            bias=True,
            batch_first=True,
            dropout=dropout,
            bidirectional=True,
        )
        self.hidden2tag = nn.Linear(2 * hidden_size, num_tags)
        self.dropout = nn.Dropout(dropout)
        self.crf = PlainCRF(num_tags)

    def forward(
        self,
        input_ids,
        token_type_ids,
        attention_mask,
        sents_mask=None,
        labels=None,
        **kwargs
    ):

        is_first = True
        for i in range(len(input_ids)):
            emb = self.plm(
                input_ids=input_ids[i],
                attention_mask=attention_mask[i],
                token_type_ids=token_type_ids[i],
                return_dict=True,
            )
            emb = self.dropout(emb.last_hidden_state)
            sorted_seq_lengths, indices = torch.sort(
                attention_mask[i].sum(-1), descending=True
            )
            _, desorted_indices = torch.sort(indices, descending=False)
            emb = emb[indices]
            out_temp = nn.utils.rnn.pack_padded_sequence(
                emb, sorted_seq_lengths.detach().cpu(), batch_first=True
            )
            out_temp, (_, _) = self.lstm_enc(out_temp)
            out_temp, _ = nn.utils.rnn.pad_packed_sequence(
                out_temp, batch_first=True, total_length=attention_mask[i].size(-1)
            )
            out_temp = out_temp[desorted_indices]

            if is_first:
                out = torch.unsqueeze(out_temp, 0)
                is_first = False
            else:
                out = torch.cat((out, torch.unsqueeze(out_temp, 0)), 0)

        out = out.max(-2)[0]
        out = self.hidden2tag(out)
        results = {"preds": self.crf.decode(out)}

        if labels is not None:

            results["loss"] = -self.crf(out, labels, sents_mask)

        return results
