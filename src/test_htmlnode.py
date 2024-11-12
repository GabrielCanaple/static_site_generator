import unittest
from htmlnode import HTMLNode


class Test_HTMLNode(unittest.TestCase):
    def test_properties_to_html_none(self):
        node = HTMLNode()
        self.assertRaises(TypeError, node.properties_to_html)

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
