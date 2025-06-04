from textnode import TextNode,TextType
from split_dilemeter import markdown_to_html_node
import os
import shutil

def main():
    copies_all_the_contents("static","public")


def copies_all_the_contents(source,dest):
    source = os.path.join(os.getcwd(), source.strip("/"))
    dest = os.path.join(os.getcwd(), dest.strip("/"))

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
        if os.path.isfile(chemin_complet) or os.path.islink(chemin_complet):
            os.remove(chemin_complet)
        elif os.path.isdir(chemin_complet):
            shutil.rmtree(chemin_complet)

if __name__ == "__main__":
    main()