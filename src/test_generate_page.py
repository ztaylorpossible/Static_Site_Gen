import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
Here is a markdown file with a title:
# This is a title
and it has some other text
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_exception(self):
        md = """
Here is a markdown file with no title:
and it has some other text
"""
        with self.assertRaises(Exception):
            title = extract_title(md)
