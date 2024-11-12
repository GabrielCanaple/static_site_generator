import unittest
from htmlnode import HTMLNode, LeafNode


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
