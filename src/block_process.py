from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block:str):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if re.match(r"^```(?:.|\n)*?```$", block, re.DOTALL):
        return BlockType.CODE

    if re.match(r"^(> .*(\n|$))+", block):
        return BlockType.QUOTE

    if re.match(r"^(- .*(\n|$))+", block):
        return BlockType.UNORDERED_LIST
    
    lines = block.strip().splitlines()
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. .+", line):
            is_ordered = False
            break
    if is_ordered and lines:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    

def extract_title(markdown):
    def extract_title(markdown):
        lines = markdown.splitlines()
        for line in lines:
            if line.startswith('# '):  # Check for H1 header (starts with a single # followed by space)
                return line[2:].strip()  # Strip the # and any leading/trailing whitespace
        raise ValueError("No H1 header found in the markdown")