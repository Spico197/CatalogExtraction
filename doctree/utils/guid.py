from typing import Iterable


def parse_guid(string: str):
    return list(map(int, string.split(".")))


def generate_guid(guid_list: Iterable):
    guid_str = ".".join(map(str, guid_list))
    return guid_str
