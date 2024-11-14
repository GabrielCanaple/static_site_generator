from textnode import TextType, TextNode, split_node_delimiter
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    children = [LeafNode(None, "hello"), LeafNode("b", "world")]
    p_node = ParentNode("p", children)
    print(p_node.to_html())

    node = TextNode(
        "This is text with a **bolded phrase** in the middle", TextType.NORMAL
    )
    print(split_node_delimiter([node], "**", TextType.BOLD))


if __name__ == "__main__":
    main()
