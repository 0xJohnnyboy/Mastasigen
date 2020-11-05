# Mastasigen!, WTF is this ?

![Hey](https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif)

Hiii, welcome on Mastasigen demo ! :)

## A static site generator

Indeed, Mastasigen! is a simple **static site generator**, it renders **markdown** files to serve you a neat design static site.
You can sneak a peek at the render in the second "article" which is actually a test file, shamelessly stolen from github.

![what](https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif)
> Ok but, what does it provide ?

Actually, nothing really fancy. It supports almost everything GFM flavor offers, and renders *3 main pages* (Home, About and Contact).
The generator supports i18n for 5 languages at the moment.You should feel free to contribute to the project as it is open source, 
but especially on the translations even if you are no python dev ninja.


The projects strengths may be its simplicity.

> Ok but, how does it work ?

![explain](https://media.giphy.com/media/5wWf7H89PisM6An8UAU/giphy.gif)

As it works in CLI, you can just automate the update with a cron on your server. 

At the creation of a site you have to edit the configuration. 
This can be done by editing the `config.yaml` file or by using the *Config Helper*, which is i18n too (English and French).
```bash
vim config.yaml
```
or
```bash
py mastasigen.py -v -i
```

![cool](https://media.giphy.com/media/2HONNTJbRhzKE/giphy.gif)

> Is that it ?

The project is evolving and new features are yet to come. Such as file deletion, in-article update, search-form etc etc.

Once again, feel free to contribute. This is my first python project and I'm not really familiar with it yet. 
Any help is welcome as long as respects conventions in `CONTRIBUTING.md`.

Thank you for reading me. 
If you want to give me money for whatever reason, please click [this link](http://paypal.me/sonicfuryFR)

![drop the mic](https://media.giphy.com/media/UTYz3M8lcTvqaVbSo9/giphy.gif)