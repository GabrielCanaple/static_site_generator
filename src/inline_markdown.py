import re
from typing import List
from textnode import TextNode, TextType


def split_node_delimiter(
    unparsed_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    pass
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
