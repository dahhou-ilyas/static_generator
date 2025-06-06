import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode,text_node_to_html_node
from textnode import TextNode,TextType
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


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()