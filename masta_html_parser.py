from html.parser import HTMLParser


class MastaParse(HTMLParser):

    def __init__(self):
        super().__init__()
        self.start_tag_list = []
        self.end_tag_list = []

    def handle_starttag(self, tag, attrs):
        self.start_tag_list.append(tag)

    def handle_endtag(self, tag):
        self.end_tag_list.append(tag)

    # Custom parser returns the missing html tag of the string
    def get_missing_closing_tag(self):
        missing_tag = [tag for tag in self.start_tag_list if tag not in self.end_tag_list]

        if not missing_tag:
            return ''

        return f'</{missing_tag[0]}>'
