import unittest
from split_dilemeter import extract_markdown_links ,extract_markdown_images,split_nodes_image,split_nodes_link,text_to_textnodes,markdown_to_blocks
from textnode import TextNode,TextType
from block_process import block_to_block_type,BlockType


class TestTextNode(unittest.TestCase):
    def test_extract_single_link(self):
        text = "Learn from [Boot.dev](https://www.boot.dev)"
        expected = [("Boot.dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_multiple_links(self):
        text = "See [Google](https://google.com) and [GitHub](https://github.com)"
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_single_image(self):
        text = "Here is an image ![cat](https://img.com/cat.png)"
        expected = [("cat", "https://img.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_multiple_images(self):
        text = "Images: ![A](url1) and ![B](url2)"
        expected = [("A", "url1"), ("B", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_links(self):
        text = "This has no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_no_images(self):
        text = "This has no images"
        self.assertEqual(extract_markdown_images(text), [])


    def test_single_image(self):
        node = TextNode(
            "Here is an image ![cat](https://img.com/cat.png)",
            TextType.TEXT
        )
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://img.com/cat.png"),
        ]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_multiple_images(self):
        node = TextNode(
            "Image1 ![a](url1) then text ![b](url2) end.",
            TextType.TEXT
        )
        expected = [
            TextNode("Image1 ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "url1"),
            TextNode(" then text ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "url2"),
            TextNode(" end.", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_image_start_and_end(self):
        node = TextNode(
            "![start](url1) middle ![end](url2)",
            TextType.TEXT
        )
        expected = [
            TextNode("start", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url2")
        ]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_image_only(self):
        node = TextNode(
            "![only](url)",
            TextType.TEXT
        )
        expected = [
            TextNode("only", TextType.IMAGE, "url")
        ]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_no_image(self):
        node = TextNode("This is just text", TextType.TEXT)
        expected = [node]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_non_text_node_untouched(self):
        node = TextNode("![shouldnot](change.png)", TextType.IMAGE, "change.png")
        expected = [node]
        self.assertListEqual(split_nodes_image([node]), expected)

    def test_single_link(self):
        node = TextNode(
            "Click [here](https://example.com) now",
            TextType.TEXT
        )
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" now", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_multiple_links(self):
        node = TextNode(
            "See [Google](https://google.com) and [GitHub](https://github.com)",
            TextType.TEXT
        )
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_link_start_and_end(self):
        node = TextNode(
            "[Start](url1) middle [End](url2)",
            TextType.TEXT
        )
        expected = [
            TextNode("Start", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("End", TextType.LINK, "url2")
        ]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_link_only(self):
        node = TextNode(
            "[only](https://only.com)",
            TextType.TEXT
        )
        expected = [
            TextNode("only", TextType.LINK, "https://only.com")
        ]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_no_link(self):
        node = TextNode("This is plain text", TextType.TEXT)
        expected = [node]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_non_text_node_untouched(self):
        node = TextNode("Should stay the same", TextType.BOLD)
        expected = [node]
        self.assertListEqual(split_nodes_link([node]), expected)

    def test_simple_bold(self):
        text = "Hello **world**!"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_combined_styles(self):
        text = "This is **bold** and _italic_ and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_image_and_link(self):
        text = "Look at ![cat](http://img.com/cat.jpg) and [GitHub](https://github.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Look at ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "http://img.com/cat.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]
        self.assertEqual(result, expected)

    def test_complex_line(self):
        text = "Start **bold** _italic_ `code` ![img](url) [link](url2)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_no_formatting(self):
        text = "Just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_heading_paragraph_list(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """.strip()

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]

        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_only_one_paragraph(self):
        markdown = "Just a simple paragraph with **bold** and `code`."
        expected = ["Just a simple paragraph with **bold** and `code`."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_blocks_with_extra_whitespace(self):
        markdown = """
    
    First block with spaces.
    
    

    Second block with tabs and newlines.
    
        """
        expected = [
            "First block with spaces.",
            "Second block with tabs and newlines."
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_all_whitespace(self):
        markdown = "   \n \n \t  "
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subheading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too many hashes"), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ndef foo():\n    return 'bar'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Not a code block (missing end backticks)
        invalid_block = "```\ndef foo():\n    return 'bar'"
        self.assertNotEqual(block_to_block_type(invalid_block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> spanning multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        invalid_block = "This is not > a valid quote"
        self.assertNotEqual(block_to_block_type(invalid_block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        invalid_block = "* Not valid\n- Valid?"
        self.assertNotEqual(block_to_block_type(invalid_block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        out_of_order_block = "1. First\n3. Third\n2. Second"
        self.assertNotEqual(block_to_block_type(out_of_order_block), BlockType.ORDERED_LIST)

        malformed_block = "1. First\n2.Second (missing space)"
        self.assertNotEqual(block_to_block_type(malformed_block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a normal paragraph.\nIt has multiple lines,\nbut no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # A single line that's just text
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()