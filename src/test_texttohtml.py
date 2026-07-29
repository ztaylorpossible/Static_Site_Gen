import unittest
from texttohtml import text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

class TestTextToHTML(unittest.TestCase):
    def test_type(self):
        node = 42
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

    def test_text_type(self):
        node = TextNode("Should raise ValueError", "InvalidTextType")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIsNotNone(html_node.props)
        if html_node.props:
            self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "meme.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is an image node")
        self.assertIsNotNone(html_node.props)
        if html_node.props:
            self.assertEqual(html_node.props["src"], "meme.jpg")
            self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_headers(self):
        md = "# This is an h1 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is an h1 header</h1></div>")
        md = "## This is an h2 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is an h2 header</h2></div>")
        md = "### This is an h3 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is an h3 header</h3></div>")
        md = "#### This is an h4 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>This is an h4 header</h4></div>")
        md = "##### This is an h5 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h5>This is an h5 header</h5></div>")
        md = "###### This is an h6 header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>This is an h6 header</h6></div>")

    def test_blockquote(self):
        md = """
> This is a quote
> and a **second** line of quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote and a <b>second</b> line of quote.</blockquote></div>")

    def test_unordered_list(self):
        md = """
- This is one item
- This is _another_ item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is one item</li><li>This is <i>another</i> item</li></ul></div>")

    def test_ordered_list(self):
        md = """
1. This is one item
2. This is `another` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is one item</li><li>This is <code>another</code> item</li></ol></div>")
