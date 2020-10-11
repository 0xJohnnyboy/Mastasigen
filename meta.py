import os
import shutil
from author import Author


class Meta:

    def __init__(self, author: Author, title, short_description,
                 long_description, lang, charset, theme, header_image, md_path, output, stylesheet, javascript):
        self.title = title
        self.short_description = short_description
        self.long_description = long_description
        self.lang = lang
        self.charset = charset
        self.theme = theme
        self.header_image = header_image
        self.author = author
        self.md_path = md_path
        self.output = output
        self.stylesheet = stylesheet
        self.javascript = javascript

    def get_meta(self):
        return [self.author.get_author(), self.title, self.short_description,
                self.long_description, self.lang, self.charset, self.theme, self.header_image, self.md_path,
                self.output, self.stylesheet, self.javascript]

    # Copies assets to the output directory.
    # Creates the directories if they don't exist, then replaces the original paths by the output ones in meta
    def copy_assets(self, preserve_styles=False, preserve_js=False):
        assets_dir = f'{self.output}/assets'
        img_dir = f'{assets_dir}/img/'
        css_dir = f'{assets_dir}/css/'
        js_dir = f'{assets_dir}/js/'

        for d in [self.output, assets_dir, img_dir, css_dir, js_dir]:
            os.path.isdir(d) is not True and os.mkdir(d)

        if self.header_image and os.path.isfile(self.header_image) is True:
            header_image_final_path = img_dir + os.path.basename(self.header_image)
            os.path.isfile(header_image_final_path) is not True and shutil.copyfile(self.header_image,
                                                                                    header_image_final_path)
            self.header_image = header_image_final_path.replace(self.output, '.')
        else:
            self.header_image = ''

        if self.author.profile_picture and os.path.isfile(self.author.profile_picture) is True:
            profile_pic_final_path = img_dir + os.path.basename(self.author.profile_picture)
            os.path.isfile(self.author.profile_picture) is True and os.path.isfile(
                profile_pic_final_path) is not True and shutil.copyfile(self.author.profile_picture,
                                                                        profile_pic_final_path)
            self.author.profile_picture = profile_pic_final_path.replace(self.output, '.')
        else:
            self.author.profile_picture = ''

        stylesheet_final_path = css_dir + os.path.basename(self.stylesheet)
        preserve_styles is False and shutil.copyfile(self.stylesheet, stylesheet_final_path)

        js_final_path = js_dir + os.path.basename(self.javascript)
        preserve_js is False and shutil.copyfile(self.javascript, js_final_path)


        self.stylesheet = stylesheet_final_path.replace(self.output, '.')
        self.javascript = js_final_path.replace(self.output, '.')
