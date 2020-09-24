import i18n

from yattag import Doc, indent
from meta import Meta
from author import Author

class Index:

    def __init__(self, cwd, meta: Meta):
        self.cwd = cwd
        self.meta = meta

    def generate(self):
        i18n.load_path.append('./translations')
        doc, tag, text = Doc().tagtext()
        doc.asis('!<DOCTYPE html>')

        with tag(f'html'):
            doc.attr(lang = self.meta.lang)

            with tag('head'):
                doc.stag('meta', lang = self.meta.lang)
                
                with tag('title'):
                    text(self.meta.title)
                # todo: handle theme
                doc.stag('link', rel = "stylesheet", src = self.meta.stylesheet)
                with tag('body'):
                    with tag('ul'):
                        with tag('li'):
                            with tag('a', href='#'):
                                text('home')
                with tag('script'):
                    doc.attr(src = self.meta.javascript)

        return indent(doc.getvalue())
