"""Split whole paragraph or sentences into pieces to add more concat actions"""
import random
from typing import Optional, List

import jieba
from rex.utils.io import load_line_json, dump_line_json
from rex.utils.progress_bar import tqdm

from doctree.data.convert import convert_json_to_node
from doctree.data.definition import Node, NodeType


def split_string(string: str, min_len: int, max_len: int) -> List[str]:
    if len(string) <= max_len:
        return [string]

    split_strings = []
    left_string = string
    while len(left_string) > 0:
        split_len = random.choice(range(min_len, max_len + 1))
        piece = left_string[:split_len]
        split_strings.append(piece)
        left_string = left_string[split_len:]
    return split_strings


def split_title(title: str, min_len: int, max_len: int) -> List[str]:
    if len(title) <= max_len:
        return [title]

    split = []
    last_string = ""
    words = jieba.lcut(title)
    for word in words:
        if len(last_string) < min_len:
            last_string += word
        else:
            split.append(last_string)
            last_string = ""
    if len(last_string) != 0:
        split.append(last_string)
    return split


def resplit_content(
    content: List[str],
    is_main_title: Optional[bool] = False,
    min_len: Optional[int] = 70,
    max_len: Optional[int] = 100,
    min_title_len: Optional[int] = 7,
    max_title_len: Optional[int] = 20,
    split_prob: Optional[float] = 0.5,
) -> List[str]:
    if is_main_title:
        if len(content) > 1:
            return content
        # 50-50 to split or not
        if random.uniform(0, 1) < split_prob:
            return split_title(content[0], min_len=min_title_len, max_len=max_title_len)
        else:
            return content

    # common content for headings and texts
    new_content = []
    for string in content:
        if random.uniform(0, 1) < split_prob:
            new_content.extend(split_string(string, min_len=min_len, max_len=max_len))
        else:
            new_content.append(string)
    return new_content


def node_traverse_update(node: Node) -> Node:
    is_main_title = False
    if node.guid == "0.0" and node.label == NodeType.Heading:
        is_main_title = True

    node.content = resplit_content(node.content, is_main_title)

    if len(node.children) > 0:
        for child in node.children:
            node_traverse_update(child)


if __name__ == "__main__":
    for dataset_name in ["train", "dev", "test"]:
        input_filepath = f"data/doc_tree_construct/zhwiki/{dataset_name}.jsonl"
        dump_filepath = f"data/doc_tree_construct/Paper/Wiki/{dataset_name}.jsonl"

        new_data = []
        for d in tqdm(load_line_json(input_filepath)):
            node = convert_json_to_node(d)
            node_traverse_update(node)
            new_data.append(node.traverse())

        dump_line_json(new_data, dump_filepath)
