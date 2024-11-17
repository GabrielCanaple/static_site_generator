import unittest

from textnode import (
    TextType,
    TextNode,
    LeafNode,
)


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

    def test_normal_textnode_to_htmlnode(self):
        text_node = TextNode("Hello World", TextType.NORMAL)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "Hello World")

    def test_bold_textnode_to_htmlnode(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<b>Bold Text</b>")

    def test_italic_textnode_to_htmlnode(self):
        text_node = TextNode("Italic Text", TextType.ITALIC)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<i>Italic Text</i>")

    def test_code_textnode_to_htmlnode(self):
        text_node = TextNode("Code Snippet", TextType.CODE)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<code>Code Snippet</code>")

    def test_link_textnode_to_htmlnode(self):
        text_node = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), '<a href="https://openai.com">OpenAI</a>')

    def test_image_textnode_to_htmlnode(self):
        text_node = TextNode("Logo", TextType.IMAGE, "https://openai.com/logo.png")
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://openai.com/logo.png" alt="Logo"></img>',
        )


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
