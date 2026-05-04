import unittest
from splitnodes import check_valid_markdown, split_nodes_delimiter, split_nodes_image, split_nodes_link
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

    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            nodes
        )

    def test_split_image_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with ending text", TextType.PLAIN)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with ending text", TextType.PLAIN)
            ],
            nodes
        )

    def test_split_no_image(self):
        node = TextNode("This text contains no image", TextType.PLAIN)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], node)

    def test_split_link_for_image(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], node)

    def test_split_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            nodes
        )

    def test_split_link_start(self):
        node = TextNode("[Boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) links", TextType.PLAIN)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            [
                TextNode("Boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" links", TextType.PLAIN),
            ],
            nodes
        )

    def test_split_no_link(self):
        node = TextNode("This text contains no link", TextType.PLAIN)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], node)

    def test_split_image_for_link(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], node)
