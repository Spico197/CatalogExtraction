from typing import List

from rex.utils.io import load_json
from rex.utils.segmentation import sent_seg


def extract_content_from_file(file_path):
    data = load_json(file_path)
    content = extract_content_from_json(data)
    return content


def extract_content_from_json(data: dict):
    content = []
    for page in data["page_list"]:
        for words_block in page["words_block_list"]:
            content.append(words_block["words_result"])

    return content


def get_pair_for_concat(content: List[str]):
    pair_list = []
    for i in range(1, len(content)):
        pair = {
            "order": str(i),
            "sentence1": content[i - 1],
            "sentence2": content[i],
        }
        pair_list.append(pair)
    return pair_list


def merge_pair_text(concat_pred: List[dict]) -> List[str]:
    if len(concat_pred) < 1:
        return []

    concat_pred.sort(key=lambda x: int(x["order"]))
    results = [concat_pred[0]["sentence1"]]

    for i in range(len(concat_pred)):
        pred = concat_pred[i]["pred_tag"]
        # sent1 has been included as idx `-1` in the last step
        curr_sent = concat_pred[i]["sentence1"]
        if not results[-1].endswith(curr_sent):
            raise ValueError(
                f"Current sentence not in the last element! curr: {curr_sent}, last: {results[-1]}"
            )

        next_sent = concat_pred[i]["sentence2"]
        # split
        if pred == 0:
            results.append(next_sent)
        else:
            results[-1] += next_sent
    return results


def get_pair_for_split(content):
    count = 0
    all_split_data = []
    last_sent = ""
    for paragraph in content:

        text = "".join(paragraph)

        sent_list = sent_seg(text, punctuations={";", "；"})

        for idx, sent in enumerate(sent_list):
            sent_pair = {
                "order": f"{count}",
                "sentence1": last_sent,
                "sentence2": sent,
            }
            if len(last_sent) > 0:
                all_split_data.append(sent_pair)
                count += 1
            last_sent = sent

    return all_split_data


def merge_pairs_by_specil(concat_pred: List[dict], concat_symbol: str) -> List[dict]:
    if len(concat_pred) < 1:
        return []

    concat_pred.sort(key=lambda x: int(x["order"]))
    results = [concat_pred[0]["sentence1"]]

    for i in range(len(concat_pred)):
        pred = concat_pred[i]["pred_tag"]
        # sent1 has been included as idx `-1` in the last step
        curr_sent = concat_pred[i]["sentence1"]
        if not results[-1].endswith(curr_sent):
            raise ValueError(
                f"Current sentence not in the last element! curr: {curr_sent}, last: {results[-1]}"
            )

        next_sent = concat_pred[i]["sentence2"]
        # split
        if pred == 0:
            results.append(next_sent)
        else:
            results[-1] += concat_symbol + next_sent
    return results
