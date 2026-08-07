from generate_page import generate_pages_recursive
from copydir import copy_dir_contents

def main():
    copy_dir_contents("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")

main()
