from textnode import TextNode,TextType
import re
from block_process import block_to_block_type,BlockType
from htmlnode import ParentNode,text_node_to_html_node,LeafNode



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown: missing closing delimiter")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)",text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text = node.text
        parts = re.split(r"!\[[^\]]+\]\([^)]+\)", text)
        images = extract_markdown_images(text)

        for i in range(len(parts)):
            if parts[i]:
                result.append(TextNode(parts[i], TextType.TEXT))
            if i < len(images):
                alt, url = images[i]
                result.append(TextNode(alt, TextType.IMAGE, url))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text = node.text
        parts = re.split(r"\[[^\]]+\]\([^)]+\)", text)
        link = extract_markdown_links(text)    
        for i in range(len(parts)):
            if parts[i]:
                result.append(TextNode(parts[i], TextType.TEXT))
            if i < len(link):
                info, url = link[i]
                result.append(TextNode(info,TextType.LINK, url))
    return result


def text_to_textnodes(text):
    # Étape 1 : créer un seul TextNode de type TEXT avec tout le texte
    nodes = [TextNode(text, TextType.TEXT)]

    # Étape 2 : découper selon les images
    nodes = split_nodes_image(nodes)

    # Étape 3 : découper selon les liens
    nodes = split_nodes_link(nodes)

    # Étape 4 : découper selon le gras (markdown **)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Étape 5 : découper selon l'italique (_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Étape 6 : découper selon les blocs de code (``)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
    
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    
    

""" 
def extract_inside_outside(text, delimiter):
    entre = []
    hors = []
    i = 0
    d_len = len(delimiter)

    while i < len(text):
        if text[i:i+d_len] == delimiter:
            start = i + d_len
            end = text.find(delimiter, start)
            if end != -1:
                entre.append(text[start:end])
                i = end + d_len
            else:
                # Si on trouve un délimiteur d'ouverture sans fermeture
                hors.append(text[i:])
                break
        else:
            next_delim = text.find(delimiter, i)
            if next_delim == -1:
                hors.append(text[i:])
                break
            else:
                hors.append(text[i:next_delim])
                i = next_delim

    return entre, hors

 """