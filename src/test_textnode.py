import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_eq(self):
        node = TextNode("This is some text", TextType.PLAIN)
        node2 = TextNode("This is different text", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_link_eq(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.PLAIN, "https://www.google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
