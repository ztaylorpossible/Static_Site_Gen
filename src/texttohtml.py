from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from converttext import markdown_to_blocks, text_to_textnodes
from blocktype import BlockType, block_to_block_type

def text_node_to_html_node(text_node):
    if type(text_node) != TextNode:
        raise TypeError()
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
    raise ValueError()

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            pre_node = ParentNode("pre", [html_node])
            nodes.append(pre_node)
        elif block_type == BlockType.HEADING:
            html_node = get_html_heading(block)
            nodes.append(html_node)
        elif block_type == BlockType.QUOTE:
            html_node = get_html_quote(block)
            nodes.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            html_node = get_html_unordered_list(block)
            nodes.append(html_node)
        elif block_type == BlockType.ORDERED_LIST:
            html_node = get_html_ordered_list(block)
            nodes.append(html_node)
        else:
            block = block.replace("\n", " ")
            html_node = ParentNode("p", text_to_children(block))
            nodes.append(html_node)
    root_node = ParentNode("div", nodes)
    return root_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = [text_node_to_html_node(n) for n in text_nodes]
    return child_nodes

def get_html_heading(text):
    heading_count = 0
    while text[0] == "#":
        heading_count += 1
        text = text[1:]
    text = text.strip()
    nodes = text_to_children(text)
    return ParentNode(f"h{heading_count}", nodes)

def get_html_quote(text):
    lines = text.split("\n")
    text = ""
    for line in lines:
        text += f" {line[1:].strip()}"
    nodes = text_to_children(text[1:])
    return ParentNode("blockquote", nodes)

def get_html_unordered_list(text):
    lines = text.split("\n")
    items = []
    for line in lines:
        items.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", items)

def get_html_ordered_list(text):
    lines = text.split("\n")
    items = []
    for line in lines:
        items.append(ParentNode("li", text_to_children(line[3:])))
    return ParentNode("ol", items)
