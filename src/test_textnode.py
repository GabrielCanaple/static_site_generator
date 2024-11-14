import unittest

from textnode import TextType, TextNode, LeafNode, split_node_delimiter


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

    def test_split_node_delimiter_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.NORMAL
        )
        self.assertEqual(
            split_node_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        self.assertEqual(
            split_node_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_italic(self):
        node = TextNode("This is text with an *italic block* word", TextType.NORMAL)
        self.assertEqual(
            split_node_delimiter([node], "*", TextType.ITALIC),
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_multiple_bold(self):
        node = TextNode(
            "This has **multiple bold** phrases **in one** sentence.", TextType.NORMAL
        )
        self.assertEqual(
            split_node_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This has ", TextType.NORMAL),
                TextNode("multiple bold", TextType.BOLD),
                TextNode(" phrases ", TextType.NORMAL),
                TextNode("in one", TextType.BOLD),
                TextNode(" sentence.", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_multiple_italic(self):
        node = TextNode(
            "This has *multiple italic* phrases *in one* sentence.", TextType.NORMAL
        )
        self.assertEqual(
            split_node_delimiter([node], "*", TextType.ITALIC),
            [
                TextNode("This has ", TextType.NORMAL),
                TextNode("multiple italic", TextType.ITALIC),
                TextNode(" phrases ", TextType.NORMAL),
                TextNode("in one", TextType.ITALIC),
                TextNode(" sentence.", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_code_at_edges(self):
        node = TextNode("`Start with code` and then `end with code`", TextType.NORMAL)
        self.assertEqual(
            split_node_delimiter([node], "`", TextType.CODE),
            [
                TextNode("Start with code", TextType.CODE),
                TextNode(" and then ", TextType.NORMAL),
                TextNode("end with code", TextType.CODE),
            ],
        )

    def test_split_node_delimiter_mixed_bold_italic(self):
        node = TextNode(
            "A **bold statement** and then an *italic phrase*.", TextType.NORMAL
        )
        result_bold = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result_bold,
            [
                TextNode("A ", TextType.NORMAL),
                TextNode("bold statement", TextType.BOLD),
                TextNode(" and then an *italic phrase*.", TextType.NORMAL),
            ],
        )
        result_italic = split_node_delimiter(result_bold, "*", TextType.ITALIC)
        self.assertEqual(
            result_italic,
            [
                TextNode("A ", TextType.NORMAL),
                TextNode("bold statement", TextType.BOLD),
                TextNode(" and then an ", TextType.NORMAL),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_consecutive_bold_italic(self):
        node = TextNode(
            "**Bold start** then continue with *italic* right after.", TextType.NORMAL
        )
        result_bold = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result_bold,
            [
                TextNode("Bold start", TextType.BOLD),
                TextNode(" then continue with *italic* right after.", TextType.NORMAL),
            ],
        )
        result_italic = split_node_delimiter(result_bold, "*", TextType.ITALIC)
        self.assertEqual(
            result_italic,
            [
                TextNode("Bold start", TextType.BOLD),
                TextNode(" then continue with ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" right after.", TextType.NORMAL),
            ],
        )


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
