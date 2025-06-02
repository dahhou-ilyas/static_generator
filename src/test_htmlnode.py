import unittest
from htmlnode import HTMLNode,LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlNode = HTMLNode("p","hello",[],{
            "href": "https://www.google.com",
            "target": "_blank",
            })
        result = htmlNode.props_to_html()
        
        self.assertEqual(result,' href="https://www.google.com" target="_blank"')

    def test_props_multiple_attributes(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        props = node.props_to_html()
        self.assertIn('href="https://example.com"', props)
        self.assertIn('target="_blank"', props)
        self.assertEqual(len(props.split()), 2)
    
    def test_props_empty(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')