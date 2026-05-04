from textnode import TextNode, TextType
from extractlinks import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        node_text = node.text
        if not check_valid_markdown(node_text, delimiter):
            raise Exception(f"Invalid markdown: {node_text}")
        split_text = node_text.split(delimiter)
        use_type = False
        for text in split_text:
            current_type = text_type if use_type else TextType.PLAIN
            new_node = TextNode(text, current_type)
            new_nodes.append(new_node)
            use_type = not use_type
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            sections = node_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_text = sections[1]
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link_text, link_url in links:
            sections = node_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            node_text = sections[1]
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.PLAIN))
    return new_nodes

def check_valid_markdown(text, delimiter):
    matching = True
    delim_length = len(delimiter)
    for i in range(len(text)):
        if i + delim_length > len(text):
            break
        sample = text[i:i+delim_length]
        if sample == delimiter:
            matching = not matching
    return matching

