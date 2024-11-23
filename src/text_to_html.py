import html
from typing import List
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes


def build_block_children_paragraph(block: str) -> List[HTMLNode]:
    return list(map(lambda textnode: textnode.to_html_node(), text_to_textnodes(block)))


def build_block_children_code(block: str) -> List[HTMLNode]:
    return list(
        map(
            lambda textnode: textnode.to_html_node(),
            text_to_textnodes(
                html.escape(block.removeprefix("```").removesuffix("```").strip())
            ),
        )
    )


def build_block_children_heading(block: str) -> tuple[str, List[HTMLNode]]:
    count = block.find(" ")
    return f"h{count}", list(
        map(
            lambda textnode: textnode.to_html_node(),
            text_to_textnodes(block[count + 1 :]),
        )
    )


def build_block_children_quote(block: str) -> List[HTMLNode]:
    return list(
        map(
            lambda textnode: textnode.to_html_node(),
            text_to_textnodes(
                "\n".join(
                    map(lambda line: line.lstrip("> ").strip(), block.split("\n"))
                )
            ),
        )
    )


def build_block_children_unordered_list(block: str) -> List[ParentNode]:
    children = list(
        map(
            lambda line: ParentNode(
                "li",
                list(
                    map(
                        lambda textnode: textnode.to_html_node(),
                        text_to_textnodes(line),
                    )
                ),
            ),
            map(
                lambda line: line.lstrip("*- ").strip(),
                block.split("\n"),
            ),
        )
    )

    return children


def build_block_children_ordered_list(block: str) -> List[ParentNode]:
    children = list(
        map(
            lambda line: ParentNode(
                "li",
                list(
                    map(
                        lambda textnode: textnode.to_html_node(),
                        text_to_textnodes(line),
                    )
                ),
            ),
            map(lambda line: line.lstrip("1234567890. ").strip(), block.split("\n")),
        )
    )

    return children


def block_to_html_node(block: str) -> ParentNode:
    block_type: BlockType = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", build_block_children_paragraph(block))
        case BlockType.HEADING:
            return ParentNode(*build_block_children_heading(block))
        case BlockType.CODE:
            return ParentNode(
                "pre", [ParentNode("code", build_block_children_code(block))]
            )
        case BlockType.QUOTE:
            return ParentNode("blockquote", build_block_children_quote(block))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", build_block_children_unordered_list(block))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", build_block_children_ordered_list(block))


def markdown_to_html_node(text: str) -> HTMLNode:
    return ParentNode(
        "div",
        list(map(lambda block: block_to_html_node(block), markdown_to_blocks(text))),
    )
