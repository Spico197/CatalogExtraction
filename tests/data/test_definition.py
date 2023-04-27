from doctree.data.definition import NodeType, RootNode, HeadingNode, TextNode


def test_traverse():
    demo_data = RootNode(
        "0",
        [
            HeadingNode(
                "0.0",
                ["Main Title", "--Second Line Title"],
                [
                    HeadingNode(
                        "0.0.0",
                        ["Heading 1"],
                        [
                            TextNode("0.0.0.0", ["text 1", "text 2"]),
                            TextNode("0.0.0.1", ["text 3"]),
                            HeadingNode(
                                "0.0.0.2",
                                ["Heading 1.1"],
                                [TextNode("0.0.0.2.0", ["text 4"])],
                            ),
                            HeadingNode(
                                "0.0.0.3",
                                ["Heading 1.2"],
                                [TextNode("0.0.0.3.0", ["text 5", "text 6"])],
                            ),
                        ],
                    ),
                    HeadingNode(
                        "0.0.1", ["heading 2"], [TextNode("0.0.1.0", ["text 7"])]
                    ),
                ],
            )
        ],
    )

    json_data = demo_data.traverse()
    gold_data = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title", "--Second Line Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["Heading 1"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": ["text 1", "text 2"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": ["text 3"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.1"],
                                "children": [
                                    {
                                        "guid": "0.0.0.2.0",
                                        "label": NodeType.Text,
                                        "content": ["text 4"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.0.3",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.2"],
                                "children": [
                                    {
                                        "guid": "0.0.0.3.0",
                                        "label": NodeType.Text,
                                        "content": ["text 5", "text 6"],
                                        "children": [],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["heading 2"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["text 7"],
                                "children": [],
                            }
                        ],
                    },
                ],
            }
        ],
    }
    assert json_data == gold_data
