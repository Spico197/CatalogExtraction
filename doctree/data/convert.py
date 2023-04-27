from typing import Optional, List

import lxml.html
from rex.utils.logging import logger

from doctree.data.definition import (
    Node,
    RootNode,
    HeadingNode,
    TextNode,
    NodeType,
    Action,
)
from doctree.utils.doc_tree_decoding import move_pointer


def line_reorder(json_obj: dict) -> List[dict]:
    node_list = []

    def traverse(node: dict):
        """only collect leaf nodes"""
        if node is None:
            return
        # not leaf node
        node_list.append(node)
        if len(node["children"]) > 0:
            for child in node["children"]:
                traverse(child)

    traverse(json_obj)
    return node_list


def html_traverse(node):
    children = node.getchildren()
    curr_text = node.text.split() if node.text is not None else []
    # empty node, except for p node in case of text missing
    if (
        len(children) == 1
        and len(curr_text) < 1
        and node.tag != "p"
        and "h" not in node.tag
        and node.tag != "html"
    ):
        return html_traverse(children[0])

    children = node.getchildren()
    curr_children = []
    curr_tag = node.tag
    curr_text = node.text.split() if node.text is not None else []

    if len(children) < 1 and len(curr_text) < 1:
        return None

    if curr_tag == "p" or ("h" in node.tag and node.tag != "html"):
        curr_text = ["".join([x.strip() for x in node.itertext()])]
        # empty p node
        if len(curr_text[0]) < 1:
            return None
    else:
        for child in children:
            # drop head links
            if child.tag == "head":
                continue

            child_texts = "".join(child.itertext()).strip()
            if (
                child.tag == "span"
                and len(child_texts) > 0
                and len(child.getchildren()) < 1
            ):
                curr_text.append(child_texts)
                continue

            new_node = html_traverse(child)
            if new_node is not None:
                if len(new_node["content"]) < 1 and len(new_node["children"]) < 1:
                    continue
                curr_children.append(new_node)

    return {"tag": curr_tag, "content": curr_text, "children": curr_children}


def convert_node_to_html(node):
    json_obj = node.traverse()
    node_list = line_reorder(json_obj)

    html = ""
    for obj in node_list:
        if obj["label"] == NodeType.Root:
            continue
        elif obj["label"] == NodeType.Heading:
            level = obj["guid"].count(".")
            html += f"<h{level}>{''.join(obj['content'])}</h{level}>"
        else:
            html += f"<p>{''.join(obj['content'])}</p>"
    return html


def convert_html_string_with_xfix(
    string: str,
    title: Optional[list] = None,
    heading_offset: Optional[int] = 0,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
):
    html = lxml.html.fromstring(string)
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format(
        node_list, title, heading_offset=heading_offset, prefix=prefix, suffix=suffix
    )
    return universal_formatted_node


def convert_to_universal_format(
    node_list,
    title: Optional[list] = None,
    heading_offset: Optional[int] = 0,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
):
    """
    Common texts with the same heading level are surrounded
        by the h* tags with special prefix or suffix strings.
        If prefix and suffix are not None, it must meet
        both requirements to convert such headings to texts.
    """
    if prefix is not None and (not isinstance(prefix, str) or len(prefix) < 1):
        raise ValueError(f"prefix: {prefix} is not valid")
    if suffix is not None and (not isinstance(suffix, str) or len(suffix) < 1):
        raise ValueError(f"suffix: {suffix} is not valid")

    # 根节点
    root = RootNode(guid="0")
    # 大标题节点
    if title is not None:
        node_list.insert(0, {"tag": "h0", "content": title, "children": []})
    # 层级
    hlabel2level = {f"h{l}": l for l in range(7)}
    level2node = {i: [] for i in range(7)}

    # 正式构建
    last_hnode = root
    base_hnode = root
    last_node = root
    last_level_num = -1
    last_level = [0]

    for node in node_list:
        if node["tag"] in {"html", "head", "link", "body"}:
            continue
        # heading
        if "h" in node["tag"]:
            h_tag = node["tag"]
            h_tag = f"h{int(h_tag[1:]) + heading_offset}"
            h_level = hlabel2level[h_tag]
            text_node = False
            NodeClass = HeadingNode
            if (
                prefix is not None
                and suffix is not None
                and node["content"][0].startswith(prefix)
                and node["content"][0].endswith(suffix)
            ):
                text_node = True
                NodeClass = TextNode
                node["content"][0] = node["content"][0][len(prefix) : -len(suffix)]
            elif prefix is not None and node["content"][0].startswith(prefix):
                text_node = True
                NodeClass = TextNode
                node["content"][0] = node["content"][0][len(prefix) :]
            elif suffix is not None and node["content"][0].endswith(suffix):
                text_node = True
                NodeClass = TextNode
                node["content"][0] = node["content"][0][: -len(suffix)]
            # sibling
            if h_level == last_level_num:
                last_level[-1] += 1
                curr_hnode = NodeClass(
                    guid=".".join(map(str, last_level)),
                    content=node["content"],
                    parent=base_hnode,
                )
            elif h_level > last_level_num:  # child
                if h_level - last_level_num != 1:
                    raise ValueError("Level(s) is skipped, check the input")
                last_level.append(0)
                curr_hnode = NodeClass(
                    guid=".".join(map(str, last_level)),
                    content=node["content"],
                    parent=last_hnode,
                )
                base_hnode = last_hnode
            else:  # ancestor node
                if len(level2node[h_level]) < 1:
                    raise ValueError(
                        "Lower level appears before high levels, check the input"
                    )
                last_level = last_level[: h_level + 2]  # + parent, + curr
                last_level[-1] += 1
                curr_hnode = NodeClass(
                    guid=".".join(map(str, last_level)),
                    content=node["content"],
                    parent=level2node[h_level][-1].parent,
                )
                base_hnode = level2node[h_level - 1][-1]

            last_node = curr_hnode
            base_hnode.add_child(curr_hnode)
            last_level_num = h_level
            if not text_node:
                last_hnode = curr_hnode
            level2node[h_level].append(curr_hnode)
        else:  # text
            if last_node.label == NodeType.Text:
                last_level[-1] += 1
            else:
                last_level.append(0)
            curr_node = TextNode(
                guid=".".join(map(str, last_level)),
                content=node["content"],
                parent=last_hnode,
            )
            last_hnode.add_child(curr_node)
            last_level_num = len(last_level)
            last_node = curr_node
            h_level = len(last_hnode.guid.split(".")) - 1
            level2node[h_level].append(curr_node)
    return root


def convert_to_universal_format_with_xfix(
    title,
    node_list,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
):
    """
    Common texts with the same heading level are surrounded
        by the h* tags with special prefix or suffix strings.
        If prefix and suffix are not None, it must meet
        both requirements to convert such headings to texts.
    """
    logger.warning(
        "`convert_to_universal_format_with_xfix()` is deprecated, use `convert_to_universal_format()` instead."
    )
    return convert_to_universal_format(node_list, title, prefix=prefix, suffix=suffix)


def filtering_node_list(node_list):
    def pass_func(node):
        flag = False
        if (
            node["tag"] not in {"html", "body", "head", "link"}
            and len(node["content"]) > 0
        ):
            flag = True
        return flag

    node_list = list(filter(pass_func, node_list))
    return node_list


def convert_html_to_line_json(html_node, filtering: Optional[bool] = True):
    json_obj = html_traverse(html_node)
    node_list = line_reorder(json_obj)
    if filtering:
        node_list = filtering_node_list(node_list)
    return node_list


def convert_json_to_node(json_obj: dict) -> Node:
    label2node_class = {"Root": RootNode, "Heading": HeadingNode, "Text": TextNode}

    def traverse(obj: dict):
        if obj["label"] == NodeType.Text and len(obj["children"]) > 0:
            raise ValueError(f"Text node has more than one child: {obj}")

        NodeClass = label2node_class[obj["label"]]
        # leaf node
        if len(obj["children"]) < 1:
            node = NodeClass(guid=obj["guid"], content=obj["content"])
            return node
        else:
            children_nodes = []
            for child in obj["children"]:
                node = traverse(child)
                children_nodes.append(node)
            if obj["label"] == "Root":
                curr_node = NodeClass(guid=obj["guid"], children=children_nodes)
            else:
                curr_node = NodeClass(
                    guid=obj["guid"], content=obj["content"], children=children_nodes
                )

            for child_node in curr_node.children:
                child_node.parent = curr_node
            return curr_node

    return traverse(json_obj)


def convert_sent_list_to_node(texts_with_labels: Optional[List[dict]]) -> Node:
    """
    decode a tree from input texts with labels

    Args:
        texts_with_labels: list of text with label for the input

    Returns:
        root node of the tree
    """
    lables = [
        "text",
        "main_title",
        "heading_1",
        "heading_2",
        "heading_3",
        "heading_4",
        "heading_5",
        "heading_6",
        "heading_7",
        "heading_8",
    ]
    root_node = RootNode(guid="0")
    past_node = root_node
    for input_dic in texts_with_labels:
        left_content = [input_dic["text"]]
        while left_content is not None:
            if past_node.label == NodeType.Root:
                if input_dic["label"] == "text":
                    action = Action.SubText
                else:
                    action = Action.SubHeading
            elif past_node.label == NodeType.Heading:
                if input_dic["label"] == "text":
                    action = Action.SubText
                else:
                    past_level = past_node.guid.count(".")
                    now_level = lables.index(input_dic["label"])
                    if past_level < now_level:
                        action = Action.SubHeading
                    else:
                        action = Action.Reduce
            elif past_node.label == NodeType.Text:
                action = Action.Reduce

            if past_node.label == NodeType.Root and action == Action.Reduce:
                logger.warning(
                    f"content {left_content} is predicted as the superior of ROOT, take it as SubText"
                )
                action = Action.SubText
            past_node, left_content = move_pointer(past_node, left_content, action)
    return root_node

def convert_tagging_text_to_node(texts_with_labels: Optional[List[dict]]) -> Node:
    """
    decode a tree from input texts with labels

    Args:
        texts_with_labels: list of text with label for the input

    Returns:
        root node of the tree
    """
    lables = [
        "text",
        "main_title",
        "heading_1",
        "heading_2",
        "heading_3",
        "heading_4",
        "heading_5",
        "heading_6",
        "heading_7",
        "heading_8",
    ]
    root_node = RootNode(guid="0")
    past_node = root_node
    for input_dic in texts_with_labels:
        left_content = input_dic["text"]
        while left_content is not None:
            if past_node.label == NodeType.Root:
                if input_dic["label"] == "text":
                    action = Action.SubText
                else:
                    action = Action.SubHeading
            elif past_node.label == NodeType.Heading:
                if input_dic["label"] == "text":
                    action = Action.SubText
                else:
                    past_level = past_node.guid.count(".")
                    now_level = lables.index(input_dic["label"])
                    if past_level < now_level:
                        action = Action.SubHeading
                    else:
                        action = Action.Reduce
            elif past_node.label == NodeType.Text:
                action = Action.Reduce

            if past_node.label == NodeType.Root and action == Action.Reduce:
                logger.warning(
                    f"content {left_content} is predicted as the superior of ROOT, take it as SubText"
                )
                action = Action.SubText
            past_node, left_content = move_pointer(past_node, left_content, action)
    return root_node
