# coding: utf-8

AUTHOR   = 'Masanori Ogino'
SITENAME = 'Brackets Salad'
SITEURL  = 'http://omasanori.github.io'

RELATIVE_URLS = True

TIMEZONE            = 'Asia/Tokyo'
DEFAULT_LANG        = 'ja'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

ARTICLE_URL           = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS       = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL      = ARTICLE_URL
ARTICLE_LANG_SAVE_AS  = ARTICLE_SAVE_AS
CATEGORY_URL          = 'blog/category/{slug}/'
CATEGORY_SAVE_AS      = 'blog/category/{slug}/index.html'
CATEGORIES_URL        = 'blog/category/'
CATEGORIES_SAVE_AS    = 'blog/category/index.html'
TAG_URL               = 'blog/tag/{slug}/'
TAG_SAVE_AS           = 'blog/tag/{slug}/index.html'
TAGS_URL              = 'blog/tag/'
TAGS_SAVE_AS          = 'blog/tag/index.html'
AUTHOR_URL            = 'blog/author/{slug}/'
AUTHOR_SAVE_AS        = 'blog/author/{slug}/index.html'
AUTHORS_URL           = 'blog/author/'
AUTHORS_SAVE_AS       = 'blog/author/index.html'
ARCHIVES_URL          = 'blog/'
ARCHIVES_SAVE_AS      = 'blog/index.html'
YEAR_ARCHIVE_URL      = 'blog/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS  = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_URL     = 'blog/{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_URL       = 'blog/{date:%Y}/{date:%m}/{date:%d}/'
DAY_ARCHIVE_SAVE_AS   = 'blog/{date:%Y}/{date:%m}/{date:%d}/index.html'

PAGE_PATHS = []

FEED_ALL_ATOM         = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM    = None # 'feeds/%s.atom.xml'
AUTHOR_FEED_ATOM      = None
AUTHOR_FEED_RSS       = None
TRANSLATION_FEED_ATOM = None

LINKS = ()

SOCIAL = ()

DEFAULT_PAGINATION = 10

DELETE_OUTPUT_DIRECTORY = True

# THEME = 'theme'
# THEME_STATIC_DIR = ''
GOOGLE_WEBMASTERS_ID = '-lHX-Eqh694tVTYA4PQWcWE_nEEkeh3PbHq8CEOqH2U'
