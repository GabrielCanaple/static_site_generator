from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import extract_markdown_links, split_node_delimiter


def main():
    children = [LeafNode(None, "hello"), LeafNode("b", "world")]
    p_node = ParentNode("p", children)
    print(p_node.to_html())

    node = TextNode(
        "This is text with a **bolded phrase** in the middle", TextType.NORMAL
    )
    print(split_node_delimiter([node], "**", TextType.BOLD))

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))


if __name__ == "__main__":
    main()
