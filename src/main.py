from generate_page import generate_page
from copydir import copy_dir_contents

def main():
    copy_dir_contents("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
