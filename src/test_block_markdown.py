import unittest
from block_markdown import (
    extract_title,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item""",
            ],
        )

    def test_markdown_to_blocks_basic(self):
        text = "This is a simple paragraph."
        self.assertEqual(
            markdown_to_blocks(text),
            ["This is a simple paragraph."],
        )

    def test_markdown_to_blocks_multiple_paragraphs(self):
        text = """This is the first paragraph.

This is the second paragraph.

This is the third paragraph."""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "This is the first paragraph.",
                "This is the second paragraph.",
                "This is the third paragraph.",
            ],
        )

    def test_markdown_to_blocks_with_list(self):
        text = """Here is a list:

1. First item
2. Second item
3. Third item

Another paragraph after the list."""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "Here is a list:",
                """1. First item
2. Second item
3. Third item""",
                "Another paragraph after the list.",
            ],
        )

    def test_markdown_to_blocks_with_heading(self):
        text = """# Heading 1

This is a paragraph under the heading.

## Subheading

This is another paragraph under a subheading."""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# Heading 1",
                "This is a paragraph under the heading.",
                "## Subheading",
                "This is another paragraph under a subheading.",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        text = """

# Header with extra newlines


This paragraph has extra newlines above and below it.



"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# Header with extra newlines",
                "This paragraph has extra newlines above and below it.",
            ],
        )

    def test_markdown_to_blocks_empty_text(self):
        text = ""
        self.assertEqual(markdown_to_blocks(text), [])

    def test_markdown_to_blocks_only_whitespace(self):
        text = "   \n   \n   "
        self.assertEqual(markdown_to_blocks(text), [])

    def test_block_to_block_type_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Smaller heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("```\ndef x(): pass\n\n\n\n```"), BlockType.CODE
        )

    def test_block_to_block_type_quotes(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(
            block_to_block_type("- Another item"), BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item"), BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("No leading markdown chars"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_edge_cases(self):
        # Empty or unknown structures default to paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_extract_title(self):
        text = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```"""
        self.assertEqual(extract_title(text), "Tolkien Fan Club")

    def test_extract_title_no_title(self):
        with self.assertRaises(ValueError):
            text = ""
            extract_title(text)


if __name__ == "__main__":
    unittest.main()
