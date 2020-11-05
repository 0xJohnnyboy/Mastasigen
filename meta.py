from __future__ import print_function, unicode_literals

import os
import shutil

import i18n
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError

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

    def config_helper(self):
        ok = False
        language = 'en'
        while ok is not True:
            choice = input('Select a language for the config helper:\n1: English \n2: Français\n')
            if choice == '1':
                language = 'en'
                ok = True
            elif choice == '2':
                language = 'fr'
                ok = True
            else:
                ok = False

        i18n.load_path.append('./translations')
        i18n.set('locale', language)

        questions = [
            {
                'type': 'expand',
                'name': 'mode',
                'message': i18n.t("config.mode"),
                'choices': [
                    {
                        'key': 's',
                        'name': i18n.t("config.mode_simple"),
                        'value': 'simple'
                    },
                    {
                        'key': 'a',
                        'name': i18n.t("config.mode_advanced"),
                        'value': 'advanced'
                    }
                ]
            },
            {
                'type': 'input',
                'name': 'site_title',
                'message': i18n.t("config.site_title"),
            },
            {
                'type': 'input',
                'name': 'site_short',
                'message': i18n.t("config.site_short"),
            },
            {
                'type': 'input',
                'name': 'site_long',
                'message': i18n.t("config.site_long"),
            },
            {
                'type': 'confirm',
                'name': 'site_lang_confirm',
                'message': i18n.t("config.site_lang_confirm", selected_language=language),
                'default': True
            },
            {
                'type': 'list',
                'name': 'site_lang',
                'message': i18n.t("config.site_lang"),
                'choices': [
                    'English',
                    'Français',
                    'Deutsch',
                    'Italiano',
                    'Español'
                ],
                'when': lambda answers: answers['site_lang_confirm'] is False
            },
            {
                'type': 'confirm',
                'name': 'site_charset_confirm',
                'message': i18n.t("config.site_charset_confirm") + i18n.t("config.recommended"),
                'default': True,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'input',
                'name': 'site_charset',
                'message': i18n.t("config.site_charset"),
                'when': lambda answers: answers['mode'] == 'advanced' and answers['site_charset_confirm'] is False
            },
            {
                'type': 'confirm',
                'name': 'site_theme_confirm',
                'message': i18n.t("config.site_theme_confirm") + i18n.t("config.recommended"),
                'default': True,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'list',
                'name': 'site_theme',
                'message': i18n.t("config.site_theme"),
                'choices': ['system', 'light', 'dark'],
                'when': lambda answers: answers['mode'] == 'advanced' and answers['site_theme_confirm'] is False
            },
            {
                'type': 'input',
                'name': 'site_header',
                'message': i18n.t("config.site_header"),
                'validate': FilePathValidator
            },
            {
                'type': 'input',
                'name': 'site_source',
                'message': i18n.t("config.site_source"),
                'default': self.md_path,
                'validate': DirPathValidator,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'input',
                'name': 'site_output',
                'message': i18n.t("config.site_output"),
                'default': self.output,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'confirm',
                'name': 'site_styles_confirm',
                'message': i18n.t("config.site_styles_confirm") + i18n.t("config.recommended"),
                'default': True,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'input',
                'name': 'site_styles',
                'message': i18n.t("config.site_styles"),
                'validate': FilePathValidator,
                'when': lambda answers: answers['mode'] == 'advanced' and answers['site_styles_confirm'] is False
            },
            {
                'type': 'confirm',
                'name': 'site_js_confirm',
                'message': i18n.t("config.site_js_confirm") + i18n.t("config.recommended"),
                'default': True,
                'when': lambda answers: answers['mode'] == 'advanced'
            },
            {
                'type': 'input',
                'name': 'site_js',
                'message': i18n.t("config.site_js"),
                'validate': FilePathValidator,
                'when': lambda answers: answers['mode'] == 'advanced' and answers['site_js_confirm'] is False
            },
            {
                'type': 'input',
                'name': 'author_name',
                'message': i18n.t("config.author_name"),
            },
            {
                'type': 'input',
                'name': 'author_mail',
                'message': i18n.t("config.author_mail"),
            },
            {
                'type': 'input',
                'name': 'author_phone',
                'message': i18n.t("config.author_phone"),
            },
            {
                'type': 'input',
                'name': 'author_github',
                'message': i18n.t("config.author_github"),
            },
            {
                'type': 'input',
                'name': 'author_avail_from',
                'message': i18n.t("config.author_avail_from"),
            },
            {
                'type': 'input',
                'name': 'author_avail_to',
                'message': i18n.t("config.author_avail_to"),
            },
            {
                'type': 'input',
                'name': 'author_profile_pic',
                'message': i18n.t("config.author_profile_pic"),
                'validate': FilePathValidator,
            },
        ]

        answers = prompt(questions)

        self.title = answers['site_title']
        self.short_description = answers['site_short']
        self.long_description = answers['site_long']
        self.lang = language if answers['site_lang_confirm'] is True else answers['site_lang'][:2].lower()
        self.header_image = answers['site_header']
        self.author = Author(
            answers['author_name'],
            answers['author_mail'],
            answers['author_phone'],
            answers['author_github'],
            answers['author_avail_from'],
            answers['author_avail_to'],
            answers['author_profile_pic']
        )
        if answers['mode'] == 'advanced':
            self.md_path = answers['site_source']
            self.output = answers['site_output']

            if answers['site_charset_confirm'] is False:
                self.charset = answers['site_charset']
            if answers['site_theme_confirm'] is False:
                self.theme = answers['site_theme']

            if answers['site_styles_confirm'] is False:
                self.stylesheet = answers['site_styles']

            if answers['site_js_confirm'] is False:
                self.javascript = answers['site_js']


class FilePathValidator(Validator):
    def validate(self, document):
        if not os.path.isfile(document.text) or document.text == '':
            raise ValidationError(
                message=i18n.t("config.error_path"),
                cursor_position=len(document.text)
            )  # Move cursor to end


class DirPathValidator(Validator):
    def validate(self, document):
        if not os.path.isdir(document.text) or document.text == '':
            raise ValidationError(
                message=i18n.t("config.error_path"),
                cursor_position=len(document.text)
            )  # Move cursor to end
