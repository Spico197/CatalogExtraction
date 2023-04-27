from doctree.data.definition import Action, NodeType, RootNode, HeadingNode
from doctree.utils import doc_tree_decoding


def test_move_pointer():
    # sub-heading
    root_node = RootNode(guid="0")
    curr_node, left_content = doc_tree_decoding.move_pointer(
        root_node, ["Heading 1"], action=Action.SubHeading
    )
    assert left_content is None
    assert curr_node.label == NodeType.Heading
    assert curr_node.content == ["Heading 1"]
    assert curr_node.parent == root_node

    # sub-text
    root_node = RootNode(guid="0")
    curr_node, left_content = doc_tree_decoding.move_pointer(
        root_node, ["Text 1"], action=Action.SubText
    )
    assert left_content is None
    assert curr_node.label == NodeType.Text
    assert curr_node.content == ["Text 1"]
    assert curr_node.parent == root_node

    # concat
    root_node = HeadingNode(guid="0", content=["heading"])
    curr_node, left_content = doc_tree_decoding.move_pointer(
        root_node, ["Text 1"], action=Action.Concat
    )
    assert left_content is None
    assert curr_node.label == NodeType.Heading
    assert curr_node.content == ["heading", "Text 1"]
    assert curr_node.parent is None

    # reduce
    root_node = RootNode(guid="0")
    heading_node = HeadingNode(guid="0.0", parent=root_node)
    root_node.children.append(heading_node)
    curr_node, left_content = doc_tree_decoding.move_pointer(
        heading_node, ["Text 1"], action=Action.Reduce
    )
    assert left_content == ["Text 1"]
    assert curr_node is root_node


def test_decode_tree():
    def predict_api(former_content, latter_content):
        content2action = {
            "ROOTtitle": Action.SubHeading,
            "titletext1": Action.SubText,
            "text1heading1": Action.Reduce,
            "titleheading1": Action.SubHeading,
            "heading1text2": Action.SubText,
        }
        input_content = "".join(former_content) + "".join(latter_content)
        return content2action[input_content]

    input_queue = ["title", "text1", "heading1", "text2"]
    root_node = doc_tree_decoding.decode_tree(predict_api, input_queue)
    assert root_node.traverse() == {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Text,
                        "content": ["text1"],
                        "children": [],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["heading1"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["text2"],
                                "children": [],
                            }
                        ],
                    },
                ],
            }
        ],
    }
