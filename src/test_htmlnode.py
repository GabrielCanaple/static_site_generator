import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class Test_HTMLNode(unittest.TestCase):
    def test_properties_to_html_none(self):
        node = HTMLNode()
        self.assertEqual("", node.properties_to_html())

    def test_properties_to_html_one(self):
        node = HTMLNode("p", "blabla", None, {"href": "http://skibidi.com"})
        self.assertEqual(node.properties_to_html(), ' href="http://skibidi.com"')

    def test_properties_to_html_multiple(self):
        node = HTMLNode(
            "b",
            "bla123hbla",
            None,
            {"href": "http://skibidi.com", "asdohf": "1837468shbk"},
        )
        self.assertEqual(
            node.properties_to_html(),
            ' href="http://skibidi.com" asdohf="1837468shbk"',
        )

    def test_leaf_node_to_html_content_none(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_node_to_html(self):
        node = LeafNode("h1", "The title", {"href": "skibidi", "ousdf": "aishof"})
        self.assertEqual(
            '<h1 href="skibidi" ousdf="aishof">The title</h1>', node.to_html()
        )

    def test_leaf_node_to_html_tag_none(self):
        node = LeafNode(None, "The title", {"href": "skibidi", "ousdf": "aishof"})
        self.assertEqual("The title", node.to_html())

    def test_parent_node_none_tag(self):
        node = ParentNode(None, [])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_none_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_empty_children(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_two_leaf_nodes(self):
        node = ParentNode("p", [LeafNode(None, "hello"), LeafNode("b", "world")])
        self.assertEqual(node.to_html(), "<p>hello<b>world</b></p>")

    def test_parent_node_four_leaf_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_node_nested(self):
        node = ParentNode(
            "h1",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode("p", [LeafNode(None, "hello"), LeafNode("b", "world")]),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<h1><b>Bold text</b>Normal text<i>italic text</i>Normal text<p>hello<b>world</b></p></h1>",
        )

    def test_parent_node_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "h1",
                            [
                                LeafNode("b", "Bold Heading"),
                                LeafNode(None, " with "),
                                LeafNode("i", "italic text"),
                            ],
                        ),
                        LeafNode(None, "Some intro text."),
                    ],
                ),
                ParentNode(
                    "article",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "This is an "),
                                LeafNode("b", "important"),
                                LeafNode(None, " message."),
                            ],
                        ),
                        ParentNode(
                            "ul",
                            [
                                ParentNode(
                                    "li",
                                    [
                                        LeafNode(None, "First item with "),
                                        LeafNode("i", "italic"),
                                    ],
                                ),
                                ParentNode(
                                    "li",
                                    [
                                        LeafNode(None, "Second item with "),
                                        LeafNode("b", "bold"),
                                    ],
                                ),
                                ParentNode(
                                    "li",
                                    [
                                        ParentNode(
                                            "ul",
                                            [
                                                ParentNode(
                                                    "li",
                                                    [LeafNode(None, "Nested item 1")],
                                                ),
                                                ParentNode(
                                                    "li",
                                                    [LeafNode(None, "Nested item 2")],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<section>"
                "<h1><b>Bold Heading</b> with <i>italic text</i></h1>"
                "Some intro text."
                "</section>"
                "<article>"
                "<p>This is an <b>important</b> message.</p>"
                "<ul>"
                "<li>First item with <i>italic</i></li>"
                "<li>Second item with <b>bold</b></li>"
                "<li><ul>"
                "<li>Nested item 1</li>"
                "<li>Nested item 2</li>"
                "</ul></li>"
                "</ul>"
                "</article>"
                "</div>"
            ),
        )
