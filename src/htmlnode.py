import unittest


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
        