from textnode import TextNode, TextType
from copydir import copy_dir_contents

def main():
    copy_dir_contents("static/", "public/")

main()
