import unittest
from text_to_html import markdown_to_html_node
from htmlnode import LeafNode, ParentNode


class TestTextToHTML(unittest.TestCase):

    def test_simple_paragraph(self):
        text = "This is a simple paragraph."
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div><p>This is a simple paragraph.</p></div>",
        )

    def test_heading(self):
        text = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "</div>",
        )

    def test_code_block(self):
        text = """```
     def hello_world():
    print("Hello, World!")
     ```"""
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<pre><code>def hello_world():\n    print(&quot;Hello, World!&quot;)</code></pre>"
            "</div>",
        )

    def test_blockquote(self):
        text = "> This is a blockquote."
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div><blockquote>This is a blockquote.</blockquote></div>",
        )

    def test_unordered_list(self):
        text = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<ul>"
            "<li>Item 1</li>"
            "<li>Item 2</li>"
            "<li>Item 3</li>"
            "</ul>"
            "</div>",
        )

    def test_ordered_list(self):
        text = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<ol>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third item</li>"
            "</ol>"
            "</div>",
        )

    def test_mixed_content(self):
        text = """# Heading

     This is a paragraph with **bold text** and *italic text*.

     > This is a blockquote.

     1. Ordered item 1
     2. Ordered item 2

     * Unordered item 1
     * Unordered item 2

     ```
    print("Code block")
     ```"""
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <b>bold text</b> and <i>italic text</i>.</p>"
            "<blockquote>This is a blockquote.</blockquote>"
            "<ol>"
            "<li>Ordered item 1</li>"
            "<li>Ordered item 2</li>"
            "</ol>"
            "<ul>"
            "<li>Unordered item 1</li>"
            "<li>Unordered item 2</li>"
            "</ul>"
            "<pre><code>print(&quot;Code block&quot;)</code></pre>"
            "</div>",
        )

    def test_list_with_formatting(self):
        text = """* Item with **bold** text
    * Another item with *italic* text
    * A `code` snippet"""
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<ul>"
            "<li>Item with <b>bold</b> text</li>"
            "<li>Another item with <i>italic</i> text</li>"
            "<li>A <code>code</code> snippet</li>"
            "</ul>"
            "</div>",
        )

    def test_code_block_with_indentation(self):
        text = """```
def hello_world():
    print("Hello, World!")
    return True
    ```"""

        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div><pre><code>def hello_world():\n    print(&quot;Hello, World!&quot;)\n    return True</code></pre></div>",
        )

    def test_multiline_blockquote(self):
        text = """> This is a blockquote.
    > It spans multiple lines.
    > It can also contain *italic* or **bold** text."""
        html_node = markdown_to_html_node(text)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            "<blockquote>"
            "This is a blockquote.\nIt spans multiple lines.\n"
            "It can also contain <i>italic</i> or <b>bold</b> text."
            "</blockquote>"
            "</div>",
        )

    def test_empty_input(self):
        text = ""
        with self.assertRaises(ValueError):
            markdown_to_html_node(text).to_html()

    def test_edge_cases(self):
        # Edge case with malformed markdown
        with self.assertRaises(Exception):
            text = """# Heading without space
    *List without space"""
            markdown_to_html_node(text)
