import unittest
from split_dilemeter import split_nodes_delimiter
from textnode import TextNode,TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node,node2)
    
    def test_url_eq_Non(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertIsNone(node.url)
    
    def test_text_noteq(self):
        node = TextNode("This is a text node tialic", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    
    def test_code_block_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_split(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("A **bold** and another **one**", TextType.TEXT)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Plain text only", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_non_text_node(self):
        node = TextNode("bolded", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is **broken", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Invalid markdown", str(context.exception))

if __name__ == "__main__":
    unittest.main()