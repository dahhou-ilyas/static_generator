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
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))

            case BlockType.HEADING:
                level = block.count("#", 0, block.find(" "))
                content = block[level+1:].strip()
                children.append(ParentNode(f"h{level}", text_to_children(content)))
            
            case BlockType.CODE:
                code_content = block.strip("`").strip()
                children.append(ParentNode("pre", [LeafNode("code", code_content)]))
            
            case BlockType.QUOTE:
                quote_text = "\n".join([line[2:] for line in block.splitlines()])
                children.append(ParentNode("blockquote", text_to_children(quote_text)))

            case BlockType.UNORDERED_LIST:
                lines = block.splitlines()
                items = [ParentNode("li", text_to_children(line[2:])) for line in lines]
                children.append(ParentNode("ul", items))

            case BlockType.ORDERED_LIST:
                lines = block.splitlines()
                items = [ParentNode("li", text_to_children(line[line.find('.')+2:])) for line in lines]
                children.append(ParentNode("ol", items))

    return ParentNode("div", children)
    
    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
    
    

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