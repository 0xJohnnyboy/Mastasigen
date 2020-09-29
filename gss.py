import os
import argparse
import codecs
import shortuuid
import time
import re

from poyo import parse_string
from meta import Meta
from author import Author
from page import Page

# parsing arguments to be used through the program
parser = argparse.ArgumentParser(
    prog='GSS',
    usage='static website generation',
    description='GSS is a static site generator. It renders html static files from markdown'
)
parser.add_argument("-v", "--verbose", action='store_true', help="prints output")
parser.add_argument("-i", "--interaction", action='store_false', help="skip user interaction")
parser.add_argument("-u", "--update", help="update existing project with new articles")
args = parser.parse_args()

verbose_print = print if args.verbose else lambda *a, **k: None
verbose_print('Starting GSS', 'Getting current working directory...')

cwd = os.getcwd()

verbose_print(cwd)
verbose_print('Reading config file...')

with codecs.open('config.yaml', encoding='utf-8') as yml_file:
    yml_string = yml_file.read()

config = parse_string(yml_string)

extras = config['extras']

author = Author(
    config['author']['name'],
    config['author']['mail'],
    config['author']['phone'],
    config['author']['github'],
    config['author']['available_from'],
    config['author']['available_until'],
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

verbose_print(meta.get_meta(), extras)
verbose_print(f'Hi, GSS is about to create {meta.title}...')

md_files_links = []


def save(content, file_name, md=False):
    if md == True and content:
        html_file_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{shortuuid.uuid()}_{file_name}.html"
        title = re.search("(<h1>.*<\/h1>)([\w\W]{0,140})", content).group(1)
        excerpt = re.search("(<h1>.*<\/h1>)([\w\W]{0,140})", content).group(2)
        md_files_links.append({
            'title': title,
            'excerpt': excerpt,
            'link': f'./{html_file_name}'
        })
    else:
        html_file_name = f'{file_name}.html'

    html_file = open(f"{config['html_path']}/{html_file_name}", "w")
    html_file.write(content)
    html_file.close()

    verbose_print(f'{file_name} successfully saved !')


def render(md_file):
    verbose_print(f'Rendering {md_file}')
    file_name = md_file[:-3]
    md_file_content = open(f"{config['md_path']}/{md_file}", "r").read()
    if md_file_content != '':
        page_content = Page(cwd, meta).render_md(md_file_content, extras)
        verbose_print(f'Sample: {page_content[:200]}')
        save(page_content, file_name, True)


files = os.listdir(config['md_path'])
rendering = [render(file) for file in files if file.endswith(".md")]

index = Page(cwd, meta).generate_index(md_files_links)
about = Page(cwd, meta).generate_about()
contact = Page(cwd, meta).generate_contact()

for f in [{'name': 'index', 'content': index},
          {'name': 'about', 'content': about},
          {'name': 'contact', 'content': contact}]:
    save(f['content'], f['name'])

verbose_print(index)