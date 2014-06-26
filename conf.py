# coding: utf-8

AUTHOR   = 'Masanori Ogino'
SITENAME = 'Brackets Salad'
SITEURL  = 'http://omasanori.github.io'

RELATIVE_URLS = True

TIMEZONE            = 'Asia/Tokyo'
DEFAULT_LANG        = 'ja'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

ARTICLE_URL           = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS       = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL      = ARTICLE_URL
ARTICLE_LANG_SAVE_AS  = ARTICLE_SAVE_AS
YEAR_ARCHIVE_SAVE_AS  = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS   = 'posts/{date:%Y}/{date:%m}/{date:%d}/index.html'

FEED_ALL_ATOM         = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM    = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

LINKS = ()

SOCIAL = ()

DEFAULT_PAGINATION = 10

DELETE_OUTPUT_DIRECTORY = True

THEME = 'theme'
GOOGLE_WEBMASTERS_ID = '-lHX-Eqh694tVTYA4PQWcWE_nEEkeh3PbHq8CEOqH2U'
