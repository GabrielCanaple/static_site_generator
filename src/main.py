from block_markdown import block_to_block_type, extract_title, markdown_to_blocks
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    split_nodes_images,
    text_to_textnodes,
)
from text_to_html import markdown_to_html_node
import os
import shutil

PUBLIC_PATH = "public/"
STATIC_PATH = "static/"


def copy_filetree(dest_dir: str, src_dir: str, dry_run: bool = False):
    if not os.path.exists(src_dir):
        raise (ValueError(f"Invalid path : {src_dir}"))
    if not dry_run:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        os.mkdir(dest_dir)

    # print(f"clearing {dest_dir}")
    __copy_filetree_rec(dest_dir, src_dir, dry_run)


def __copy_filetree_rec(dest_dir: str, src_dir: str, dry_run: bool = False):
    # print(f"exploring {src_dir}")
    for elem in os.listdir(src_dir):
        elem_path_src = os.path.join(src_dir, elem)
        elem_path_dest = os.path.join(dest_dir, elem)
        if os.path.isfile(elem_path_src):
            if not dry_run:
                shutil.copy(elem_path_src, elem_path_dest)
            # print(f"copying file {elem_path_src} to {elem_path_dest}")
        else:
            if not dry_run:
                os.mkdir(elem_path_dest)
            # print(f"making directory {elem_path_dest}")
            __copy_filetree_rec(elem_path_dest, elem_path_src, dry_run)


def generate_page(dest_path: str, src_path: str, template_path: str):
    print(f"Generating page {src_path} to {dest_path} using {template_path}")
    with open(src_path) as src_file, open(template_path) as template_file:
        src_text = src_file.read()
        template_text = template_file.read()

        src_html = markdown_to_html_node(src_text).to_html()
        src_title = extract_title(src_text)

        dest_text = template_text.replace("{{ Title }}", src_title).replace(
            "{{ Content }}", src_html
        )

        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        with open(dest_path, "x") as dest_file:
            dest_file.write(dest_text)


def generate_page_recursive(dest_dir: str, src_dir: str, template_path: str):
    for elem in os.listdir(src_dir):
        elem_path_src = os.path.join(src_dir, elem)
        elem_path_dest = os.path.join(dest_dir, elem.replace(".md", ".html"))
        if os.path.isfile(elem_path_src):
            generate_page(elem_path_dest, elem_path_src, template_path)
        else:
            generate_page_recursive(elem_path_dest, elem_path_src, template_path)


def main():
    copy_filetree("public", "static")
    generate_page_recursive("public", "content", "template.html")


if __name__ == "__main__":
    main()
