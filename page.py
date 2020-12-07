import time
import i18n
import markdown2
import emoji
import re
import math

from yattag import Doc, indent
from masta_html_parser import MastaParse
from meta import Meta


# Generates a tile with an excerpt for the index and secures the excerpt for possible missing closing tags.
def generate_tile(md_file_link: {}):
    doc, tag, text = Doc().tagtext()

    excerpt = md_file_link['excerpt']
    parser = MastaParse()
    parser.feed(excerpt)
    missing_tag = parser.get_missing_closing_tag()

    if missing_tag:
        excerpt = f'{excerpt[:-len(missing_tag)]} {missing_tag}'

    if '<' in excerpt[-4:]:
        excerpt = excerpt[:-4]

    with tag('div', klass='excerpts__item'):
        with tag('a', href=f"{md_file_link['link']}", klass='excerpts__item__link'):
            doc.asis(md_file_link['title'])

        doc.asis(excerpt)

    return indent(doc.getvalue())


# Replaces emoticons by their emoji aliases equivalent in string
def emoticons_to_emoji(content):
    content = re.sub(":-\)", ":smile:", content)
    content = re.sub(":-\(", ":worried:", content)
    content = re.sub("8-\)", ":sunglasses:", content)
    content = re.sub(";\)", ":wink:", content)
    content = re.sub(":-\/", ":confused:", content)

    return content


class Page:

    def __init__(self, cwd, meta: Meta):
        self.cwd = cwd
        self.meta = meta

    # Generates a page structure with doctype, head etc.
    def generate(self, page_title=''):
        i18n.load_path.append('./translations')
        i18n.set('locale', self.meta.lang)
        i18n.set('fallback', 'en')

        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        doc.asis(f'<html lang={self.meta.lang} theme={self.meta.theme}>')

        with tag('head'):
            with tag('title'):
                if page_title == '':
                    text(self.meta.title)
                else:
                    text(f'{page_title} - {self.meta.title}')

            doc.stag('meta', charset=f'{self.meta.charset}')
            doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1.0')

            doc.stag('link', rel="stylesheet", href=f"{self.meta.stylesheet}")

        doc.asis('<body>')

        with tag('ul', klass="menu"):
            with tag('li', klass="menu__item", id="home"):
                with tag('a', href='./index.html'):
                    with tag('button'):
                        text(i18n.t('menu.home'))

            with tag('li', klass="menu__item", id="about"):
                with tag('a', href='./about.html'):
                    with tag('button'):
                        text(i18n.t('menu.about'))

            with tag('li', klass="menu__item"):
                with tag('a', href='./contact.html', id="contact"):
                    with tag('button'):
                        text(i18n.t('menu.contact'))

            with tag('li', klass="menu__item", id='theme-toggle'):
                with tag('a'):
                    with tag('button'):
                        doc.asis('<i class="menu__item__theme-toggle fas"></i>')

        with tag('header'):
            self.meta.author.profile_picture != '' and doc.stag(
                'img',
                src=f"{self.meta.author.profile_picture}",
                klass="profile-pic",
                alt=f'{self.meta.author.name} profile picture'
            )
            self.meta.header_image != '' and doc.stag(
                'img',
                src=f"{self.meta.header_image}",
                klass="header-image",
                alt='header background'
            )

            with tag('h1', klass='welcome'):
                text(i18n.t(
                    'menu.welcome',
                    author_name=self.meta.author.name
                ))

        return indent(doc.getvalue())

    # Adds the footer, script tags and closing tags to the generated html content
    def close_html(self, file_content):
        doc, tag, text = Doc().tagtext()

        with tag('footer', klass='footer'):
            text('Powered by ')
            with tag('a', href='https://github.com/Sonicfury/Mastasigen'):
                text('Mastasigen!')

        font_awesome = '<script src="https://kit.fontawesome.com/51fc2db30d.js" crossorigin="anonymous"></script>'
        custom_js = f'<script src="{self.meta.javascript}">'

        return file_content + indent(doc.getvalue()) + f'</body>{font_awesome + custom_js}</script></html>'

    # Generates the html base and renders markdown content into an html article.
    # return value doesn't use "indent" because it messes with code blocks
    def render_md(self, md_file_content, extras):
        f = self.generate()

        estimated_time = self.get_reading_time(md_file_content)

        article = markdown2.markdown(md_file_content, extras=extras)
        article = emoticons_to_emoji(article)
        article = emoji.emojize(article, use_aliases=True, variant="emoji_type")

        doc, tag, text = Doc().tagtext()

        with tag('article'):
            with tag('span', klass='article__date'):
                text(time.strftime(f'%Y %b %d - %H:%M {estimated_time}'))
            doc.asis(article)

        return self.close_html(f + doc.getvalue())

    # Generates the html base for the About page
    def generate_about(self):
        f = self.generate(i18n.t('menu.about'))

        doc, tag, text = Doc().tagtext()

        with tag('div', klass='about'):
            with tag('h2', klass='about__title'):
                text(i18n.t('menu.about'))

            with tag('p', klass='about__description'):
                text(self.meta.long_description)

        return self.close_html(f + indent(doc.getvalue()))

    # Generates the html base for the Contact page
    def generate_contact(self):
        f = self.generate(i18n.t('menu.contact'))

        i18n.load_path.append('./translations')
        i18n.set('locale', self.meta.lang)
        i18n.set('fallback', 'en')

        doc, tag, text = Doc().tagtext()

        with tag('div', klass='contact'):
            with tag('h2', klass='contact__title'):
                text(i18n.t('menu.contact'))

            with tag('span', klass='contact__message'):
                text(i18n.t('contact.intro') + '!')

            with tag('span', klass='contact__phone'):
                text(i18n.t(
                    'contact.phone',
                    opening_hour=self.meta.author.available_from,
                    closing_hour=self.meta.author.available_until
                ) + ':')

                with tag('a', href=f'tel:{self.meta.author.phone}', klass='contact__phone__link'):
                    doc.asis('<i class="fas fa-phone"></i>')

            with tag('span', klass='contact__mail'):
                text(i18n.t('contact.mail') + ':')

                with tag('a', href=f'mailto:{self.meta.author.mail}?subject=contact', klass='contact__mail__link'):
                    doc.asis('<i class="far fa-paper-plane"></i>')

        return self.close_html(f + indent(doc.getvalue()))

    # Generates index, and a tile for each article that has been previously rendered
    def generate_index(self, md_file_links: []):
        f = self.generate()

        doc, tag, text = Doc().tagtext()

        with tag('div', klass='excerpts'):
            for md_file_link in md_file_links:
                doc.asis(generate_tile(md_file_link))

        return self.close_html(f + indent(doc.getvalue()))

    # Updates the index by inserting a tile before the existing ones for each article that has been previously rendered
    def update_index(self, md_file_links: []):
        index = open(f'{self.meta.output}/index.html', "r", encoding="utf-8").read()
        excerpts = index.find('<div class="excerpts__item">')

        doc, tag, text = Doc().tagtext()

        for md_file_link in md_file_links:
            doc.asis(generate_tile(md_file_link))

        return index[:excerpts] + indent(doc.getvalue()) + index[excerpts:]

    # Returns a string containing the estimated time to read the content passed as an argument.
    # One can read about 200 words per minute so the maths are number of words divided by 200, times 60 to get seconds,
    # rounded to superior value.
    def get_reading_time(self, content):
        i18n.load_path.append('./translations')
        i18n.set('locale', self.meta.lang)
        i18n.set('fallback', 'en')

        nb_words = len(content.split())
        seconds = math.ceil((nb_words / 200) * 60)
        estimated_time = time.strftime(f'~ %M {i18n.t("article.read")}', time.gmtime(seconds))

        return estimated_time
