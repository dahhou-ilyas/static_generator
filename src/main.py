from textnode import TextNode,TextType
from split_dilemeter import markdown_to_html_node
def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    node = markdown_to_html_node(md)
    html = node.to_html()

    print(html)


if __name__ == "__main__":
    main()