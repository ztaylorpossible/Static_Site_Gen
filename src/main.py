import sys
from generate_page import generate_pages_recursive
from copydir import copy_dir_contents

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    copy_dir_contents("static/", "docs/")
    generate_pages_recursive(base_path, "content", "template.html", "docs")

main()
