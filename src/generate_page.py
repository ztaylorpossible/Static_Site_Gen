import os
from os.path import isdir

from texttohtml import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")

def get_file_contents(path):
    file = open(path)
    contents = file.read()
    file.close()
    return contents

def write_to_file(path, contents):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    with open(path, "w") as f:
        f.write(contents)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    write_to_file(dest_path, html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for entry in contents:
        full_path = os.path.join(os.path.abspath(dir_path_content), entry)
        if os.path.isfile(full_path):
            file_path = os.path.join(dir_path_content, entry)
            new_entry = entry.split(".")[0] + ".html"
            dest_path = os.path.join(dest_dir_path, new_entry)
            generate_page(file_path, template_path, dest_path)
        elif os.path.isdir(full_path):
            next_content = os.path.join(dir_path_content, entry)
            next_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(next_content, template_path, next_dest)
