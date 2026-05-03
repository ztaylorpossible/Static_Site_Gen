import unittest
from splitnodes import check_valid_markdown, split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodes(unittest.TestCase):
    def test_valid_markdown_empty(self):
        teststring = ""
        self.assertTrue(check_valid_markdown(teststring, "**"))
        self.assertTrue(check_valid_markdown(teststring, "_"))
        self.assertTrue(check_valid_markdown(teststring, "`"))

    def test_valid_markdown_none(self):
        teststring = "This is plain text"
        self.assertTrue(check_valid_markdown(teststring, "**"))
        self.assertTrue(check_valid_markdown(teststring, "_"))
        self.assertTrue(check_valid_markdown(teststring, "`"))

    def test_valid_markdown_wrong(self):
        teststring = "This has **invalid markdown"
        self.assertFalse(check_valid_markdown(teststring, "**"))
        self.assertTrue(check_valid_markdown(teststring, "_"))
        self.assertTrue(check_valid_markdown(teststring, "`"))

    def test_valid_markdown_correct(self):
        teststring = "This has **bold**, _italic_, and `code` text."
        self.assertTrue(check_valid_markdown(teststring, "**"))
        self.assertTrue(check_valid_markdown(teststring, "_"))
        self.assertTrue(check_valid_markdown(teststring, "`"))

    def test_valid_markdown_mixed(self):
        teststring = "This has **bold**, _italic, and `code`` text."
        self.assertTrue(check_valid_markdown(teststring, "**"))
        self.assertFalse(check_valid_markdown(teststring, "_"))
        self.assertFalse(check_valid_markdown(teststring, "`"))

    def test_split_plain(self):
        node = TextNode("This is some plain text", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(node, nodes[0])
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(node, nodes[0])
        self.assertEqual(len(nodes), 1)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(node, nodes[0])
        self.assertEqual(len(nodes), 1)

    def test_split_mismatch(self):
        node = TextNode("This text has **mismatched_ markdown", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(node, nodes[0])

    def test_split_skip(self):
        bold_node = TextNode("This text is **all** bold", TextType.BOLD)
        italic_node = TextNode("This text is _all_ italic", TextType.ITALIC)
        code_node = TextNode("This text is `all` code", TextType.CODE)
        nodes = split_nodes_delimiter([bold_node, italic_node, code_node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], bold_node)
        self.assertEqual(nodes[1], italic_node)
        self.assertEqual(nodes[2], code_node)
        nodes = split_nodes_delimiter([bold_node, italic_node, code_node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], bold_node)
        self.assertEqual(nodes[1], italic_node)
        self.assertEqual(nodes[2], code_node)
        nodes = split_nodes_delimiter([bold_node, italic_node, code_node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], bold_node)
        self.assertEqual(nodes[1], italic_node)
        self.assertEqual(nodes[2], code_node)

    def test_split_bold(self):
        node = TextNode("This **text** has **bold** text", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This ")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " has ")
        self.assertEqual(nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(nodes[3].text, "bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[4].text, " text")
        self.assertEqual(nodes[4].text_type, TextType.PLAIN)

    def test_split_start_bold(self):
        node = TextNode("**This** starts with bold", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text, "This")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " starts with bold")
        self.assertEqual(nodes[2].text_type, TextType.PLAIN)

    def test_split_end_bold(self):
        node = TextNode("This ends with **bold**", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This ends with ")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, "")
        self.assertEqual(nodes[2].text_type, TextType.PLAIN)

    def test_split_mixed(self):
        node = TextNode("This has **bold**, _italic_, and `code` text", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, ", ")
        self.assertEqual(nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, ", and ")
        self.assertEqual(nodes[4].text_type, TextType.PLAIN)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " text")
        self.assertEqual(nodes[6].text_type, TextType.PLAIN)
