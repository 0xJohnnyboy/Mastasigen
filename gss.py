import os
import markdown2
import argparse
import codecs

from poyo import parse_string
from meta import Meta
from author import Author
from extra import Extra
from index_generator import Index

# parsing arguments to be used through the program
parser = argparse.ArgumentParser(prog='GSS', usage='static website generation', description='GSS is a static site generator. It renders html static files from markdown')
parser.add_argument("-v", "--verbose", action='store_true', help="prints output")
parser.add_argument("-i", "--interaction", action='store_false', help="skip user interaction")
parser.add_argument("-u", "--update", help="update existing project with new articles")
args = parser.parse_args()

verboseprint = print if args.verbose else lambda *a, **k: None
verboseprint('Getting current working directory...')

cwd = os.getcwd()

verboseprint(cwd)
verboseprint('Reading config file...')

with codecs.open('config.yaml', encoding='utf-8') as yml_file:
    yml_string = yml_file.read()

config = parse_string(yml_string)

extras = Extra(
        config['extras']['code_friendly'],
        config['extras']['fenced_code_blocks'],
        config['extras']['cuddled_lists'],
        )

author = Author(
        config['author']['name'], 
        config['author']['mail'],
        config['author']['phone'], 
        config['author']['profile_picture']
        )

meta = Meta(
        author, 
        config['title'], 
        config['short_description'], 
        config['long_description'],
        config['lang'], 
        config['charset'], 
        config['theme'],
        config['stylesheet'],
        config['javascript']
        )


verboseprint(meta.get_meta(), extras.get_extras())
verboseprint(f"Hi, GSS is about to create {meta.title}...")

index = Index(cwd, meta)
index_content = index.generate()
print(index_content)

#def render(md_file):
#    args.verbose && print(f'Rendering {md_file}')
#    file_name = md_file[:-3]
#    f = open(f'{args.md_path}/{md_file}', "r")
#    rendered_md = markdown2.markdown(f.read())
#    html_file_name = f'{file_name}.html'
#    html_file = open(f'{args.html_path}/{html_file_name}',"w")
#    html_file.write(rendered_md)
#    args.verbose && print(f'{html_file_name} created !}')
#    html_file.close()
#
#files = os.listdir(args.md_path)
#files = [render(file) for file in files if file.endswith(".md")]
