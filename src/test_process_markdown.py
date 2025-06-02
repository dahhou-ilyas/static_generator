import unittest
from split_dilemeter import extract_markdown_links ,extract_markdown_images

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