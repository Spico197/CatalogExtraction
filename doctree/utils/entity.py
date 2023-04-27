import functools
from collections import defaultdict
from typing import DefaultDict, List, Tuple

from rex.utils.tagging import get_entities_from_tag_seq


def extract_entities_from_tags(tags):
    role2entities = get_entities_from_tag_seq(["x"] * len(tags), tags)
    entities = set(functools.reduce(lambda x, y: x + y, role2entities.values(), []))
    return [(ent[2], ent[3], ent[1]) for ent in entities]


def get_entities_from_start2endtable_seq(
    chars: List[str], start2endtable: List[List], label_encoder
) -> DefaultDict[str, List[Tuple]]:
    """从golden数据中的start_end_table中提取出(ent,role_type,start,end) 用于后续与pred对比得到prf"""
    seq_len = len(chars)
    entities = defaultdict(list)
    for i in range(seq_len):
        for j in range(i, seq_len):
            if start2endtable[i][j] > 0:
                role_type = label_encoder.decode([start2endtable[i][j]])[0]
                entities[role_type].append(
                    ("".join(chars[i : j + 1]), role_type, i, j + 1)
                )
    return entities


def get_entities_from_tuples_seq(
    chars: List[str], tuples: List[Tuple], label_encoder
) -> DefaultDict[str, List[Tuple]]:
    """
    从模型decode得到的(start,end,role_id)得到(ent,role_type,start,end) 用于后续与golden对比得到prf
    注意：从模型decode出来的结果中，end的位置已经+1，所以下面不再+1
    """
    entities = defaultdict(list)
    for one_tuple in tuples:
        if not (0 <= one_tuple[0] <= one_tuple[1] <= len(chars)):
            continue
        role_type = label_encoder.decode([one_tuple[2]])[0]
        entities[role_type].append(
            (
                "".join(chars[one_tuple[0] : one_tuple[1]]),
                role_type,
                one_tuple[0],
                one_tuple[1],
            )
        )
    return entities
