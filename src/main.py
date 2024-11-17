from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    split_nodes_images,
    text_to_textnodes,
)


def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))


if __name__ == "__main__":
    main()
