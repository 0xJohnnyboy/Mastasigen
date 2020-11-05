import os
import argparse
import textwrap

import shortuuid
import time
import re
import yaml
import sys
from pyfiglet import Figlet
from meta import Meta
from author import Author
from page import Page


class Mastasigen:
    def __init__(self):
        self.version = '1.2-beta'
        self.parser = argparse.ArgumentParser(
            prog='Mastasigen!',
            usage='static website generation',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(f'{Figlet(font="slant").renderText("Mastasigen!")}\n\n '
                                        f'Mastasigen! is a static site generator. '
                                        f'It renders html static files from markdown.\n '
                                        f'v{self.version}'))
        self.parser.add_argument("-v", "--verbose", action='store_true', help="prints output")
        self.parser.add_argument("-V", "--version", action='store_true', help="prints version")
        self.parser.add_argument("-i", "--interaction", action='store_true', help="config helper")
        self.parser.add_argument("-u", "--update", action='store_true',
                                 help="update existing project with new articles")
        self.args = self.parser.parse_args()

        if self.args.version is True:
            print(f"v{self.version}")
            sys.exit()

        self.verbose_print = print if self.args.verbose else lambda *a, **k: None

        self.args.verbose and print(Figlet(font='slant').renderText('Mastasigen!'))
        self.verbose_print(f"version: {self.version}")
        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Starting Mastasigen!")
        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Getting current working directory...")

        self.cwd = os.getcwd()

        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : current working directory: {self.cwd}")
        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Reading config file...")

        # Extracts config from config.yaml, and creates extras, author and meta objects.
        with open("config.yaml", 'r', encoding="utf-8") as yaml_file:
            try:
                self.config = yaml.safe_load(yaml_file)
            except yaml.YAMLError as exc:
                self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] {exc}")

        self.extras = self.config['extras']

        self.author = Author(
            self.config['author']['name'],
            self.config['author']['mail'],
            self.config['author']['phone'],
            self.config['author']['github'],
            self.config['author']['available_from'],
            self.config['author']['available_until'],
            self.config['author']['profile_picture']
        )

        self.meta = Meta(
            self.author,
            self.config['title'],
            self.config['short_description'],
            self.config['long_description'],
            self.config['lang'],
            self.config['charset'],
            self.config['theme'],
            self.config['header_image'],
            self.config['md_path'],
            self.config['output'],
            self.config['stylesheet'],
            self.config['javascript'],
        )

        if self.args.interaction is True:
            self.meta.config_helper()

        # Copies assets in the output directory, preserves styles and javascript in case this is an update
        if self.args.update is True:
            self.meta.copy_assets(True, True)
        else:
            self.meta.copy_assets()

        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : META: \n{self.meta.get_meta()}")
        self.verbose_print(
            f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : EXTRAS:\n {self.extras}")
        self.verbose_print(
            f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Hi, Mastasigen! is about to create {self.meta.title}...")

        self.md_files_links = []
        self.rendered_files_count = 0

        files = os.listdir(self.config['md_path'])
        rendering = [self.render(file) for file in files if file.endswith(".md")]

        # In case this is normal run, creates index, about and contact pages and calls the "save" function for each.
        # Otherwise, if md files have been rendered, it updates the excerpts tiles in the index.
        if self.args.update is False:
            index = Page(self.cwd, self.meta).generate_index(self.md_files_links)
            about = Page(self.cwd, self.meta).generate_about()
            contact = Page(self.cwd, self.meta).generate_contact()

            for f in [
                {'name': 'index', 'content': index},
                {'name': 'about', 'content': about},
                {'name': 'contact', 'content': contact}
            ]:
                self.save(f['content'], f['name'])

        elif self.rendered_files_count > 0:
            self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Updating index\n",)
            index = Page(self.cwd, self.meta).update_index(self.md_files_links)
            self.save(index, 'index')
        else:
            self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Nothing to update")

    # Checks if file already exists. If not, creates a unique file name with shortuuid.
    # Then it extracts the first <h1> title, and a 350 characters excerpt of the
    # document and stores them along with the html file name (required for index excerpt tiles creation/update)
    # It finally creates the html file.
    def save(self, content, file_name, md=False):
        if self.args.update is True:
            for o in os.listdir(self.meta.output):
                if md is True and file_name in o:
                    self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : {file_name} already exists")

                    return

        if md is True and content:
            self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : creating file {file_name}")

            html_file_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{shortuuid.uuid()}_{file_name}.html"
            title = re.search("(<h1>.*<\/h1>)(([\w\W]{0,350})</article>|([\w\W]{0,350}))", content).group(1).replace(
                '</h1>',
                f'<span class="excerpt__item__date">{time.strftime("%Y %b %d - %H:%M")}</span></h1>')
            excerpt = re.search("(<h1>.*<\/h1>)(([\w\W]{0,350})</article>|([\w\W]{0,350}))", content).group(2)[:-10]
            self.md_files_links.append({
                'title': title,
                'excerpt': excerpt,
                'link': f'./{html_file_name}'
            })
            self.rendered_files_count += 1
            self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : {title} {excerpt} {html_file_name}")
        else:
            html_file_name = f'{file_name}.html'

        html_file = open(f"{self.config['output']}/{html_file_name}", "w", encoding="utf-8")
        html_file.write(content)
        html_file.close()

        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] {file_name} successfully saved !")

    def render(self, md_file):
        self.verbose_print(f"[{time.strftime('%Y_%m_%d-%H:%M:%S')}] : Rendering {md_file}")
        file_name = md_file[:-3]
        md_file_content = open(f"{self.config['md_path']}/{md_file}", "r", encoding="utf-8").read()

        if md_file_content != '':
            page_content = Page(self.cwd, self.meta).render_md(md_file_content, self.extras)
            self.save(page_content, file_name, True)


mastasigen = Mastasigen()
