from textnode import TextNode,TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        # On ne modifie que les TextNode de type TEXT
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