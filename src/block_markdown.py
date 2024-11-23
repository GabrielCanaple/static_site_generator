from typing import List
from enum import Enum
from functools import reduce


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> List[str]:
    return list(
        filter(
            lambda line: line != "",
            map(lambda line: line.strip(" \n"), text.split("\n\n")),
        )
    )


def block_to_block_type(text: str) -> BlockType:
    text = text.strip()
    lines = list(map(lambda line: line.strip(), text.split("\n")))
    i = 1

    if text.startswith("#"):
        return BlockType.HEADING
    elif len(lines) > 1 and text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    elif text.startswith("> ") and reduce(
        lambda sum, _: sum + 1,
        filter(lambda line: line.startswith("> "), lines),
        0,
    ) == len(lines):
        return BlockType.QUOTE
    elif text.startswith("* ") and reduce(
        lambda sum, _: sum + 1,
        filter(lambda line: line.startswith("* "), lines),
        0,
    ) == len(lines):
        return BlockType.UNORDERED_LIST
    elif text.startswith("- ") and reduce(
        lambda sum, _: sum + 1,
        filter(lambda line: line.startswith("- "), lines),
        0,
    ) == len(lines):
        return BlockType.UNORDERED_LIST
    elif text.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
