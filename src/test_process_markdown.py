import unittest
from split_dilemeter import extract_markdown_links ,extract_markdown_images,split_nodes_image,split_nodes_link
from textnode import TextNode,TextType


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