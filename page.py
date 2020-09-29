import i18n
import markdown2

from yattag import Doc, indent
from gss_html_parser import GssHtmlParser
from meta import Meta


def generate_link(md_file_link: {}):
    doc, tag, text = Doc().tagtext()

    excerpt = md_file_link['excerpt']
    parser = GssHtmlParser()
    parser.feed(excerpt)

    if parser.get_missing_closing_tag():
        excerpt = f'{excerpt[:-len(parser.get_missing_closing_tag())]} {parser.get_missing_closing_tag()}'

    with tag('div', klass='excerpts__item'):
        with tag(
                'a',
                href=f"{md_file_link['link']}",
                klass='excerpts__item__link'
        ):
            doc.asis(md_file_link['title'])
        doc.asis(excerpt)

    return indent(doc.getvalue())


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
        doc.asis(f'<html lang={self.meta.lang}>')

        with tag('head'):
            with tag('title'):
                text(self.meta.title)

            # todo: handle theme
            doc.stag('link', rel="stylesheet", src=self.meta.stylesheet)

        doc.asis('<body>')

        with tag('header'):
            with tag('ul', klass="menu"):
                with tag('li', klass="menu__item", id="home"):
                    with tag('a', href='./index.html'):
                        text(i18n.t('menu.home'))

                with tag('li', klass="menu__item", id="about"):
                    with tag('a', href='./about.html'):
                        text(i18n.t('menu.about'))

                with tag('li', klass="menu__item"):
                    with tag('a', href='./contact.html', id="contact"):
                        text(i18n.t('menu.contact'))

            with tag('h1', klass='welcome'):
                text(i18n.t(
                    'menu.welcome',
                    author_name=self.meta.author.name
                ))

        return indent(doc.getvalue())

    def close_html(self, file_content):
        return file_content + f'</body><script src="{self.meta.javascript}"></script></html>'

    def render_md(self, md_file_content, extras):
        f = self.generate()

        article = markdown2.markdown(md_file_content, extras=extras)

        doc, tag, text = Doc().tagtext()

        with tag('article'):
            doc.asis(article)

        return self.close_html(f + indent(doc.getvalue()))

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
