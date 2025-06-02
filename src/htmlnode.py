import unittest
from textnode import TextType,TextNode

class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag=tag
        self.value=value
        self.children=children or []
        self.props=props or {}
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = " ".join(f'{key}="{value}"' for key , value in self.props.items())
        return " "+result
    
    def __repr__(self):
        return (
            f"HTMLNode(tag={repr(self.tag)}, "
            f"value={repr(self.value)}, "
            f"children={repr(self.children)}, "
            f"props={repr(self.props)})"
        )
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a non-None 'value'")
        
        super().__init__(tag, value , children=[], props=props)

    def to_html(self):
        if not self.tag:
            return self.value
        
        return f'<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>'
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required for Parrent Node")
        if self.children is None:
            raise ValueError("children is required for Parrent Node")
        
        result = f'<{self.tag}>'
        for chld in self.children:
            result = result + chld.to_html()
        return result+f'</{self.tag}>'
    

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.TEXT:
            return LeafNode("a",text_node,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception(f"{text_node.text_type} note defindef")