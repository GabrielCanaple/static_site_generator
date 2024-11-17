import re
from typing import List
from textnode import TextNode, TextType


def split_nodes_delimiter(
    unparsed_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    new_nodes = []

    for node in unparsed_nodes:

        # important case, if you don't do that the special type will get overwritten
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        node_text_split = node.text.split(delimiter)

        # check for wrong markdown syntax
        if len(node_text_split) % 2 == 0:
            raise Exception("Error while parsing : invalid markdown.")

        is_of_text_type = (
            False  # the first substring is always normal text (can be empty)
        )
        for substr in node_text_split:
            # ignore empty substrings
            if substr == "":
                is_of_text_type = not is_of_text_type
                continue

            if is_of_text_type:
                new_nodes.append(TextNode(substr, text_type))
            else:
                new_nodes.append(TextNode(substr, TextType.NORMAL))
            is_of_text_type = not is_of_text_type

    return new_nodes


def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    regex: str = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.finditer(regex, text)
    return list(map(lambda match: (match.group(1), match.group(2)), matches))


def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    regex: str = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.finditer(regex, text)
    return list(map(lambda match: (match.group(1), match.group(2)), matches))


def split_nodes_images(unparsed_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in unparsed_nodes:
        # We assume there are no nested links within special types
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        images: List[tuple[str, str]] = extract_markdown_images(node.text)
        rest: str = node.text  # The text we have yet to parse
        for image in images:
            first_part, rest = rest.split(f"![{image[0]}]({image[1]})", 1)
            if first_part != "":
                new_nodes.append(TextNode(first_part, TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        if rest != "":
            new_nodes.append(TextNode(rest, TextType.NORMAL))

    return new_nodes


def split_nodes_links(unparsed_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in unparsed_nodes:
        # We assume there are no nested links within special types
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        links: List[tuple[str, str]] = extract_markdown_links(node.text)
        rest: str = node.text  # The text we have yet to parse
        for link in links:
            first_part, rest = rest.split(f"[{link[0]}]({link[1]})", 1)
            if first_part != "":
                new_nodes.append(TextNode(first_part, TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        if rest != "":
            new_nodes.append(TextNode(rest, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text) -> List[TextNode]:
    nodes = split_nodes_images([TextNode(text, TextType.NORMAL)])
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
