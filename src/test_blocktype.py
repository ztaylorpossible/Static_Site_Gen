import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_heading_none(self):
        block_type = block_to_block_type("Not a paragraph")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_one(self):
        block_type = block_to_block_type("# Is a heading")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_one_no_space(self):
        block_type = block_to_block_type("#Is not a heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_six(self):
        block_type = block_to_block_type("###### Is a heading")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_too_many(self):
        block_type = block_to_block_type("####### Is not a heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_mixed(self):
        block_type = block_to_block_type("##!#`# Is not a heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_multiline_code(self):
        block_type = block_to_block_type(
"""```
Is a code block
```"""
        )
        self.assertEqual(block_type, BlockType.CODE)

    def test_multiline_code_inline(self):
        block_type = block_to_block_type(
"""```Is not a code block```"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_multiline_code_two_lines(self):
        block_type = block_to_block_type(
"""```
Is a code block```"""
        )
        self.assertEqual(block_type, BlockType.CODE)

    def test_multiline_code_two_start_ticks(self):
        block_type = block_to_block_type(
"""``
Is not a code block```"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_multiline_code_two_end_ticks(self):
        block_type = block_to_block_type(
"""```
Is not a code block``"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_multiline(self):
        block_type = block_to_block_type(
"""> Is a quote block
> With multiple
>Lines"""
        )
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_inline(self):
        block_type = block_to_block_type("> Is a quote block")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_wrong(self):
        block_type = block_to_block_type(
"""> Is not a quote block
# With multiple
>Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_multiline(self):
        block_type = block_to_block_type(
"""- Is an unordered list
- With multiple
- Lines"""
        )
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_inline(self):
        block_type = block_to_block_type("- Is an unordered list")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed(self):
        block_type = block_to_block_type(
"""- Is not an unordered list
> With multiple
- Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_missing_space(self):
        block_type = block_to_block_type(
"""- Is not an unordered list
- With multiple
-Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_multiline(self):
        block_type = block_to_block_type(
"""1. Is an ordered list
2. With multiple
3. Lines"""
        )
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_inline(self):
        block_type = block_to_block_type("1. Is an ordered list")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_mixed(self):
        block_type = block_to_block_type(
"""1. Is not an ordered list
- With multiple
2. Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        block_type = block_to_block_type(
"""1. Is not an unordered list
2. With multiple
3.Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_unordered(self):
        block_type = block_to_block_type(
"""1. Is not an ordered list
3. With multiple
2. Lines"""
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)
