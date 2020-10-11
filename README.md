# Mastasigen!

Mastasigen! is a markdown static blog generator. It lets you generate and update a blog from markdown articles.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install -r requirements.txt
```

## Usage

Start with config.yaml, this file lets you fine tune your blog to generate !

```yaml
title: 'Mastasigen!' Here is the title of your blog.
lang: 'fr' Mastasigen! handles i18n for english, french, german, italian, and español.
charset: 'utf-8'
theme: 'system' Default theme is system. Choices are 'system', 'light' and 'dark'

header_image: './assets/img/kian-lem.jpg' This one isn't required, its the background header image. 
                                          This is the path of the original file, the generator will copy it 
                                          into the output folder.

short_description: This is the short description for the <meta> info.
long_description: |
  This description will fill the "about" page ! Write it wisely !

author: These info will help generate the content and are required for the generator to work properly.
  name: 'John Doe' That's your name that will be displayed on the blog.
  mail: 'johndoe@mail.com'
  phone: '+33611223344' Don't forget international prefix
  github: 'https://github.com/Sonicfury'
  available_from: '9 AM' Hours your are available for calling ! 
  available_until: '7 PM'
  profile_picture: './assets/img/vicky-hladynets.jpg' Same as header image !

The following are extras for the markdown2 lib, modify at your own risks !
extras: # Documentation on https://github.com/trentm/python-markdown2/wiki/Extras
  - code-friendly
  - cuddled-lists
  - fenced-code-blocks
  - tables
  - footnotes
  - smarty-pants
  - numbering
  - tables
  - strike
  - spoiler

md_path: './md_files' The input path where you will store you original markdown files !
output: './www' The output path, where will lay your blog

Modify those at your own risks !
stylesheet: './assets/css/style.css'
javascript: './assets/js/script.js'
```

Once you're done with config.yaml, just put some markdown files to render and run the following command
```bash
python3 mastasigen.py
```

You can add `-v` or `--verbose` to make it verbose.

Next time, to update your blog, add the `-u` or `--update` argument. This will only update the excerpt tiles in index and render the new markdown files

## Contributing
Please see CONTRIBUTING.md
## Coffee
[Buy me a coffee](http://paypal.me/sonicfuryFR) 
## License
[MIT](https://choosealicense.com/licenses/mit/)