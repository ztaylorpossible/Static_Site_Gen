from textnode import TextNode, TextType

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

