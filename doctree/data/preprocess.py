import json

from doctree.data import RootNode, TextNode, HeadingNode


demo_data = RootNode(
    [
        "0",
        HeadingNode(
            "0.0",
            ["Main Title", "--Second Line Title"],
            [
                HeadingNode(
                    "0.0.0",
                    ["Heading 1"],
                    [
                        TextNode("0.0.0-0", ["text 1", "text 2"]),
                        TextNode("0.0.0-1", ["text 3"]),
                        HeadingNode(
                            "0.0.0.0",
                            ["Heading 1.1"],
                            [TextNode("0.0.1.1-0", ["text 4"])],
                        ),
                        HeadingNode(
                            "0.0.0.1",
                            ["Heading 1.2"],
                            [TextNode("0.0.0.1-0", ["text 5", "text 6"])],
                        ),
                    ],
                ),
                HeadingNode("0.0.1", ["heading 2"], [TextNode("0.0.1-0", ["text 7"])]),
            ],
        ),
    ]
)
