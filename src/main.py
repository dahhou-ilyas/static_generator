import sys
import os
import shutil
from textnode import TextNode, TextType
from split_dilemeter import markdown_to_html_node
from block_process import extract_title

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copies_all_the_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copies_all_the_contents(source, dest):
    source = os.path.join(os.getcwd(), source.strip("/"))
    dest = os.path.join(os.getcwd(), dest.strip("/"))

    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        vider_dossier(dest)

    for item in os.listdir(source):
        src_item = os.path.join(source, item)
        dest_item = os.path.join(dest, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item)
        else:
            shutil.copy2(src_item, dest_item)

def vider_dossier(dossier):
    for nom in os.listdir(dossier):
        chemin_complet = os.path.join(dossier, nom)
        try:
            if os.path.isfile(chemin_complet) or os.path.islink(chemin_complet):
                os.unlink(chemin_complet)
            elif os.path.isdir(chemin_complet):
                shutil.rmtree(chemin_complet)
        except Exception as e:
            print(f"Erreur lors de la suppression de {chemin_complet}: {e}")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as filemd:
        md_contenu = filemd.read()
    with open(template_path, 'r') as htmlfile:
        html_contenu = htmlfile.read()

    html_node = markdown_to_html_node(md_contenu)
    html_string = html_node.to_html()
    title = extract_title(md_contenu)

    html_contenu = html_contenu.replace("{{ Title }}", title)
    html_contenu = html_contenu.replace("{{ Content }}", html_string)

    html_contenu = html_contenu.replace('href="/','href="' + basepath)
    html_contenu = html_contenu.replace('src="/','src="' + basepath)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as html_final:
        html_final.write(html_contenu)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for name in files:
            if name.endswith(".md"):
                relative_path = root.replace(dir_path_content, "")
                dest_dir = os.path.join(dest_dir_path, relative_path.strip("/"))
                dest_file = os.path.join(dest_dir, name.replace(".md", ".html"))
                generate_page(os.path.join(root, name), template_path, dest_file, basepath)

if __name__ == "__main__":
    main()