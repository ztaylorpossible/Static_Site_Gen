from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(text_block):
    if is_heading(text_block):
        return BlockType.HEADING
    if is_multiline_code(text_block):
        return BlockType.CODE
    if is_quote(text_block):
        return BlockType.QUOTE
    if is_unordered_list(text_block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(text_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_heading(text_block):
    if len(text_block) == 0 or text_block[0] != "#":
        return False
    start = text_block.split(' ')[0]
    for i in range(len(start)):
        if i >= 6:
            return False
        if start[i] != "#":
            return False
    return True

def is_multiline_code(text_block):
    if len(text_block) < 7:
        return False
    if text_block[:4] != "```\n":
        return False
    if text_block[-3:] != "```":
        return False
    return True

def is_quote(text_block):
    if len(text_block) == 0:
        return False
    lines = text_block.split("\n")
    for line in lines:
        if len(line) == 0 or line[0] != ">":
            return False
    return True

def is_unordered_list(text_block):
    if len(text_block) == 0:
        return False
    lines = text_block.split("\n")
    for line in lines:
        if len(line) < 2 or line[0:2] != "- ":
            return False
    return True

def is_ordered_list(text_block):
    if len(text_block) == 0:
        return False
    lines = text_block.split("\n")
    for i in range(len(lines)):
        if len(lines[i]) < 3:
            return False
        if lines[i][0:3] != f"{i+1}. ":
            return False
    return True
