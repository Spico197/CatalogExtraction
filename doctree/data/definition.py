from enum import Enum
from copy import deepcopy as dcopy
from typing import List, Optional, Any


class Action(str, Enum):
    NULL = "NULL"
    SubHeading = "SubHeading"
    SubText = "SubText"
    Concat = "Concat"
    Reduce = "Reduce"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class ShiftReduceAction(str, Enum):
    Shift = "Shift"
    Reduce = "Reduce"

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class NodeType(str, Enum):
    Node = "Node"
    Root = "Root"
    Text = "Text"
    Heading = "Heading"

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class Node:
    """
    Each node may have multiple children,
        but has only one (or zero, if it is ROOT) parent.

    Args:
        guid: global identifier, can be the outline level identifier
        content: list of content of current node
        label: type of current node
        children: list of children nodes
        parent: parent node
    """

    def __init__(
        self,
        guid: Optional[str] = "",
        label: Optional[int] = None,
        parent: Optional[Any] = None,
    ):
        self.guid = guid
        self.content = []
        self.label = label
        self.children = []
        self.parent = parent

    def add_child(self, node):
        self.children.append(node)

    def extend_children(self, nodes):
        self.children.extend(nodes)

    def add_content(self, content):
        self.content.append(content)

    def extend_content(self, contents):
        self.content.extend(contents)

    def __getitem__(self, name: str):
        if name in {"guid", "content", "label", "children", "parent"}:
            return getattr(self, name)
        else:
            raise ValueError(f"{name} not found in {self}")

    def val(self):
        return {
            "guid": dcopy(self.guid),
            "label": dcopy(self.label),
            "content": dcopy(self.content),
            "children": dcopy(self.children),
        }

    def traverse(self):
        """pre-order traversal, return a json-like dict"""
        if len(self.children) < 1:
            return self.val()
        val = self.val()
        new_children = list()
        for node in val["children"]:
            node = node.traverse()
            new_children.append(node)
        val["children"] = new_children
        return val

    def __str__(self) -> str:
        return f"<Node {self.label}: {self.guid}>"

    def __repr__(self) -> str:
        return str(self)


class RootNode(Node):
    def __init__(
        self, guid: Optional[str] = "", children: Optional[List[Node]] = list()
    ):
        super().__init__(guid=guid, label=NodeType.Root, parent=None)
        self.add_content("ROOT")
        self.extend_children(children)


class TextNode(Node):
    def __init__(
        self,
        guid: Optional[str] = "",
        content: Optional[List[str]] = list(),
        parent: Optional[Node] = None,
    ):
        super().__init__(guid=guid, label=NodeType.Text, parent=parent)
        self.extend_content(content)


class HeadingNode(Node):
    def __init__(
        self,
        guid: Optional[str] = "",
        content: Optional[List[str]] = list(),
        children: Optional[List[Node]] = list(),
        parent: Optional[Node] = None,
    ):
        super().__init__(
            guid=guid,
            label=NodeType.Heading,
            parent=parent,
        )
        self.extend_children(children)
        self.extend_content(content)


class Stack(object):
    def __init__(self) -> None:
        super().__init__()

        self.root = None
        self.node_list = None
        self.pointer = None
