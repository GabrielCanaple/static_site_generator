import unittest

from textnode import TextType, TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_url_default(self):
        node_1 = TextNode("this is a text node", TextType.BOLD)
        node_2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node_1, node_2)

    def test_eq(self):
        node_1 = TextNode("this is a text node", TextType.BOLD, "http://google.fr")
        node_2 = TextNode("this is a text node", TextType.BOLD, "http://google.fr")
        self.assertEqual(node_1, node_2)

    def test_not_eq_text(self):
        node_1 = TextNode("This is a text node", TextType.BOLD, "http://google.fr")
        node_2 = TextNode("this is a text node", TextType.BOLD, "http://google.fr")
        self.assertNotEqual(node_1, node_2)

    def test_not_eq_url(self):
        node_1 = TextNode("This is a text node", TextType.ITALIC)
        node_2 = TextNode("this is a text node", TextType.ITALIC, "http://google.fr")
        self.assertNotEqual(node_1, node_2)

    def test_not_eq_text_type(self):
        node_1 = TextNode("This is a text node", TextType.NORMAL)
        node_2 = TextNode("this is a text node", TextType.BOLD, "http://google.fr")
        self.assertNotEqual(node_1, node_2)


if __name__ == "__main__":
    unittest.main()
