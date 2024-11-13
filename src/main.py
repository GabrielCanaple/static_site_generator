from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    children = [LeafNode(None, "hello"), LeafNode("b", "world")]
    p_node = ParentNode("p", children)
    print(p_node.to_html())


if __name__ == "__main__":
    main()
