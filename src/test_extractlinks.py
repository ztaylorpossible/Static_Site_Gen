import unittest
from extractlinks import extract_markdown_images, extract_markdown_links

single_image_text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
multi_image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIH.gif) and ![obi wan](https://i.imgur.com/jJRm4Vk.jpeg)"
multi_link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(single_image_text)
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images(multi_image_text)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIH.gif"), ("obi wan", "https://i.imgur.com/jJRm4Vk.jpeg")], matches)
        matches = extract_markdown_images(multi_link_text)
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(single_image_text)
        self.assertEqual([], matches)
        matches = extract_markdown_links(multi_image_text)
        self.assertEqual([], matches)
        matches = extract_markdown_links(multi_link_text)
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
