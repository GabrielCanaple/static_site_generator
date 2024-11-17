import unittest
from textnode import TextType, TextNode
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_delimiter_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.NORMAL
        )
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_delimiter_italic(self):
        node = TextNode("This is text with an *italic block* word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.ITALIC),
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
            split_nodes_delimiter([node], "**", TextType.BOLD),
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
            split_nodes_delimiter([node], "*", TextType.ITALIC),
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
            split_nodes_delimiter([node], "`", TextType.CODE),
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
        result_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result_bold,
            [
                TextNode("A ", TextType.NORMAL),
                TextNode("bold statement", TextType.BOLD),
                TextNode(" and then an *italic phrase*.", TextType.NORMAL),
            ],
        )
        result_italic = split_nodes_delimiter(result_bold, "*", TextType.ITALIC)
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
        result_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result_bold,
            [
                TextNode("Bold start", TextType.BOLD),
                TextNode(" then continue with *italic* right after.", TextType.NORMAL),
            ],
        )
        result_italic = split_nodes_delimiter(result_bold, "*", TextType.ITALIC)
        self.assertEqual(
            result_italic,
            [
                TextNode("Bold start", TextType.BOLD),
                TextNode(" then continue with ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" right after.", TextType.NORMAL),
            ],
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_v2(self):
        text = "Check out these images: ![Image1](http://example.com/image1.png)![Image2](http://example.com/image2.png) end."
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("Image1", "http://example.com/image1.png"),
                ("Image2", "http://example.com/image2.png"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_node_images(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_node_images_consecutive(self):
        node = TextNode(
            "Check out these images: ![Image1](http://example.com/image1.png)![Image2](http://example.com/image2.png) end.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check out these images: ", TextType.NORMAL),
                TextNode("Image1", TextType.IMAGE, "http://example.com/image1.png"),
                TextNode("Image2", TextType.IMAGE, "http://example.com/image2.png"),
                TextNode(" end.", TextType.NORMAL),
            ],
        )

    def test_split_node_images_no_images(self):
        node = TextNode(
            "This text has no images, just normal content.", TextType.NORMAL
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This text has no images, just normal content.", TextType.NORMAL
                ),
            ],
        )

    def test_split_node_images_at_start(self):
        node = TextNode(
            "![start image](http://example.com/start.png) begins the sentence.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("start image", TextType.IMAGE, "http://example.com/start.png"),
                TextNode(" begins the sentence.", TextType.NORMAL),
            ],
        )

    def test_split_node_images_at_end(self):
        node = TextNode(
            "The sentence ends with an image ![end image](http://example.com/end.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("The sentence ends with an image ", TextType.NORMAL),
                TextNode("end image", TextType.IMAGE, "http://example.com/end.png"),
            ],
        )

    def test_split_node_images_multiple_with_text(self):
        node = TextNode(
            "Here is ![Image1](http://example.com/img1.png), followed by some text, then another ![Image2](http://example.com/img2.png).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.NORMAL),
                TextNode("Image1", TextType.IMAGE, "http://example.com/img1.png"),
                TextNode(", followed by some text, then another ", TextType.NORMAL),
                TextNode("Image2", TextType.IMAGE, "http://example.com/img2.png"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_images_invalid_format(self):
        node = TextNode(
            "This is an invalid image markdown ![Invalid Image]", TextType.NORMAL
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is an invalid image markdown ![Invalid Image]",
                    TextType.NORMAL,
                ),
            ],
        )

    def test_split_node_images_special_characters_in_url(self):
        node = TextNode(
            "Check out this image: ![Cool Image](http://example.com/img%20with%20spaces.png).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check out this image: ", TextType.NORMAL),
                TextNode(
                    "Cool Image",
                    TextType.IMAGE,
                    "http://example.com/img%20with%20spaces.png",
                ),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_images_with_code(self):
        node = TextNode(
            "Here is a `code block` followed by an image ![Code Image](http://example.com/code.png).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "Here is a `code block` followed by an image ", TextType.NORMAL
                ),
                TextNode("Code Image", TextType.IMAGE, "http://example.com/code.png"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_links_basic(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) for great tutorials.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Visit ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" for great tutorials.", TextType.NORMAL),
            ],
        )

    def test_split_node_links_with_code(self):
        node = TextNode(
            "Here is a `code block` followed by a link to [Docs](http://example.com/docs).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "Here is a `code block` followed by a link to ", TextType.NORMAL
                ),
                TextNode("Docs", TextType.LINK, "http://example.com/docs"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_links_special_characters_in_url(self):
        node = TextNode(
            "Check [Example](http://example.com/query?search=test&lang=en).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check ", TextType.NORMAL),
                TextNode(
                    "Example",
                    TextType.LINK,
                    "http://example.com/query?search=test&lang=en",
                ),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_links_no_links(self):
        node = TextNode(
            "This text does not contain any markdown links.", TextType.NORMAL
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This text does not contain any markdown links.", TextType.NORMAL
                ),
            ],
        )

    def test_split_node_links_consecutive(self):
        node = TextNode(
            "Links: [Link1](http://example.com/1)[Link2](http://example.com/2).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Links: ", TextType.NORMAL),
                TextNode("Link1", TextType.LINK, "http://example.com/1"),
                TextNode("Link2", TextType.LINK, "http://example.com/2"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_links_at_end(self):
        node = TextNode(
            "The sentence ends with a link to [End Site](http://example.com).",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("The sentence ends with a link to ", TextType.NORMAL),
                TextNode("End Site", TextType.LINK, "http://example.com"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_split_node_links_at_start(self):
        node = TextNode(
            "[Start link](http://example.com) begins the sentence.", TextType.NORMAL
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start link", TextType.LINK, "http://example.com"),
                TextNode(" begins the sentence.", TextType.NORMAL),
            ],
        )

    def test_split_node_links_multiple(self):
        node = TextNode(
            "Check [Google](https://www.google.com) or [YouTube](https://www.youtube.com) for more info.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check ", TextType.NORMAL),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode(" or ", TextType.NORMAL),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" for more info.", TextType.NORMAL),
            ],
        )

    def test_split_node_links_invalid_format(self):
        node = TextNode(
            "Here is an invalid link markdown [Invalid Link]", TextType.NORMAL
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "Here is an invalid link markdown [Invalid Link]", TextType.NORMAL
                ),
            ],
        )

    def test_text_to_textnodes_basic(self):
        text = "This is a plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("This is a plain text.", TextType.NORMAL)],
        )

    def test_text_to_textnodes_start_end(self):
        text = "**Bold at start** and *italic at end*"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Bold at start", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic at end", TextType.ITALIC),
            ],
        )

    def test_text_to_textnodes_consecutive(self):
        text = "**Bold**`code`*italic*"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("code", TextType.CODE),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_text_to_textnodes_mixed(self):
        text = "Visit *our* site **now**: [Boot.dev](https://boot.dev)."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Visit ", TextType.NORMAL),
                TextNode("our", TextType.ITALIC),
                TextNode(" site ", TextType.NORMAL),
                TextNode("now", TextType.BOLD),
                TextNode(": ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_link(self):
        text = "Check [Google](http://google.com) for more info."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Check ", TextType.NORMAL),
                TextNode("Google", TextType.LINK, "http://google.com"),
                TextNode(" for more info.", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_image(self):
        text = "Here is an image: ![alt text](http://image.url)."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Here is an image: ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "http://image.url"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_code(self):
        text = "This is a `code block`."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_italic(self):
        text = "This is *italic* text."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_complex(self):
        text = "This **bold** text has `code`, *italic*, [link](http://example.com), and ![image](http://image.url)."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text has ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(", ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(", and ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "http://image.url"),
                TextNode(".", TextType.NORMAL),
            ],
        )
