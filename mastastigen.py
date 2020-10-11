import os
import sys
import argparse
import shortuuid
import time
import re
import yaml

from meta import Meta
from author import Author
from page import Page

# parsing arguments to be used through the program
parser = argparse.ArgumentParser(
    prog='Mastasigen!',
    usage='static website generation',
    description='Mastasigen! is a static site generator. It renders html static files from markdown'
)
parser.add_argument("-v", "--verbose", action='store_true', help="prints output")
parser.add_argument("-i", "--interaction", action='store_false', help="skip user interaction")
parser.add_argument("-u", "--update", action='store_true', help="update existing project with new articles")
args = parser.parse_args()

verbose_print = print if args.verbose else lambda *a, **k: None

verbose_print(time.strftime('%Y_%m_%d-%H:%M:%S'))
verbose_print('\n\nStarting Mastasigen!\n\n\n')
verbose_print('Getting current working directory...\n', '=======================================\n')

cwd = os.getcwd()

verbose_print(cwd)
verbose_print('Reading config file...\n', '=======================================\n')

with open("config.yaml", 'r') as yaml_file:
    try:
        config = yaml.safe_load(yaml_file)
    except yaml.YAMLError as exc:
        verbose_print(exc)

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
    config['header_image'],
    config['md_path'],
    config['output'],
    config['stylesheet'],
    config['javascript'],
)

if args.update is True:
    meta.copy_assets(True, True)
else:
    meta.copy_assets()

# sys.exit('stop')


verbose_print(f'META: \n{meta.get_meta()}\n')
verbose_print(f'EXTRAS:\n {extras}\n', '=======================================\n')
verbose_print(f'Hi, Mastasigen! is about to create {meta.title}...\n', '=======================================\n')

md_files_links = []
rendered_files_count = 0

def save(content, file_name, md=False):
    if args.update is True:
        for o in os.listdir(meta.output):
            if md is True and file_name in o:
                verbose_print(f'{file_name} already exists\n')

                return

    if md is True and content:
        verbose_print(f'creating file {file_name}\n')

        html_file_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{shortuuid.uuid()}_{file_name}.html"
        title = re.search("(<h1>.*<\/h1>)(([\w\W]{0,350})</article>|([\w\W]{0,350}))", content).group(1).replace(
            '</h1>',
            f'<span class="excerpt__item__date">{time.strftime("%Y %b %d - %H:%M")}</span></h1>')
        excerpt = re.search("(<h1>.*<\/h1>)(([\w\W]{0,350})</article>|([\w\W]{0,350}))", content).group(2)[:-10]
        md_files_links.append({
            'title': title,
            'excerpt': excerpt,
            'link': f'./{html_file_name}'
        })

        verbose_print(title, excerpt, html_file_name)
    else:
        html_file_name = f'{file_name}.html'

    html_file = open(f"{config['output']}/{html_file_name}", "w")
    html_file.write(content)
    html_file.close()

    rendered_files_count += 1
    verbose_print(f'{file_name} successfully saved !\n')


def render(md_file):
    verbose_print(time.strftime('%Y_%m_%d-%H:%M:%S'))
    verbose_print(f'Rendering {md_file}')
    file_name = md_file[:-3]
    md_file_content = open(f"{config['md_path']}/{md_file}", "r").read()

    if md_file_content != '':
        page_content = Page(cwd, meta).render_md(md_file_content, extras)
        save(page_content, file_name, True)


files = os.listdir(config['md_path'])
rendering = [render(file) for file in files if file.endswith(".md")]

if args.update is False:
    index = Page(cwd, meta).generate_index(md_files_links)
    about = Page(cwd, meta).generate_about()
    contact = Page(cwd, meta).generate_contact()

    for f in [
        {'name': 'index', 'content': index},
        {'name': 'about', 'content': about},
        {'name': 'contact', 'content': contact}
    ]:
        save(f['content'], f['name'])
elif rendered_files_count > 0:
    verbose_print(time.strftime('%Y_%m_%d-%H:%M:%S'))
    verbose_print('Updating index\n', '=======================================\n')
    index = Page(cwd, meta).update_index(md_files_links)
    save(index, 'index')
else:
    verbose_print('=======================================\n')
    verbose_print(time.strftime('%Y_%m_%d-%H:%M:%S'))
    verbose_print('Nothing to update\n')