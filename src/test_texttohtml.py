import unittest
from texttohtml import text_node_to_html_node
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
        self.assertEqual(html_node.value, None)
        self.assertIsNotNone(html_node.props)
        if html_node.props:
            self.assertEqual(html_node.props["src"], "meme.jpg")
            self.assertEqual(html_node.props["alt"], "This is an image node")
