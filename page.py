import time
import i18n
import markdown2
import emoji
import re
import math

from yattag import Doc, indent
from gss_html_parser import GssHtmlParser
from meta import Meta


def generate_link(md_file_link: {}):
    doc, tag, text = Doc().tagtext()

    excerpt = md_file_link['excerpt']
    parser = GssHtmlParser()
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

    def generate(self):
        i18n.load_path.append('./translations')
        i18n.set('locale', self.meta.lang)
        i18n.set('fallback', 'en')

        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        doc.asis(f'<html lang={self.meta.lang} theme={self.meta.theme}>')

        with tag('head'):
            with tag('title'):
                text(self.meta.title)

            doc.stag('meta', charset=f'{self.meta.charset}')

            # todo: handle theme
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
            doc.stag('img', src=f"{self.meta.author.profile_picture}", klass="profile-pic")
            doc.stag('img', src=f"{self.meta.header_image}", klass="header-image")

            with tag('h1', klass='welcome'):
                text(i18n.t(
                    'menu.welcome',
                    author_name=self.meta.author.name
                ))

        return indent(doc.getvalue())

    def close_html(self, file_content):
        doc, tag, text = Doc().tagtext()

        with tag('footer', klass='footer'):
            text('Powered by ')
            with tag('a', href='https://github.com/Sonicfury/Mastasigen'):
                text('Mastasigen!')

        font_awesome = '<script src="https://kit.fontawesome.com/51fc2db30d.js" crossorigin="anonymous"></script>'
        custom_js = f'<script src="{self.meta.javascript}">'

        return file_content + indent(doc.getvalue()) + f'</body>{font_awesome + custom_js}</script></html>'

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

    def generate_about(self):
        f = self.generate()

        doc, tag, text = Doc().tagtext()

        with tag('div', klass='about'):
            with tag('h2', klass='about__title'):
                text(i18n.t('menu.about'))

            with tag('p', klass='about__description'):
                text(self.meta.long_description)

        return self.close_html(f + indent(doc.getvalue()))

    def generate_contact(self):
        f = self.generate()

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

    def generate_index(self, md_file_links: []):
        f = self.generate()

        doc, tag, text = Doc().tagtext()

        with tag('div', klass='excerpts'):
            for md_file_link in md_file_links:
                doc.asis(generate_link(md_file_link))

        return self.close_html(f + indent(doc.getvalue()))

    def get_reading_time(self, content):
        i18n.load_path.append('./translations')
        i18n.set('locale', self.meta.lang)
        i18n.set('fallback', 'en')

        nb_words = len(content.split())
        seconds = math.ceil((nb_words / 200) * 60)
        estimated_time = time.strftime(f'~ %M {i18n.t("article.read")}', time.gmtime(seconds))

        return estimated_time
