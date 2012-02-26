# -*- coding: utf-8 -*-

# Django settings for newblog project.

import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

#
# Create an empty file called "devlocal" to enable local development
#
IS_LOCAL = os.path.exists(os.path.join(PROJECT_PATH, "devlocal"))

# 
# Create an empty file named "debug" to enable debug 
#
DEBUG = os.path.exists(os.path.join(PROJECT_PATH, "debug"))

HAVE_GRAPPELLI = os.path.exists(os.path.join(PROJECT_PATH, 'grappelli'))
HAVE_FILEMANAGER = os.path.exists(os.path.join(PROJECT_PATH, 'filemanager'))
HAVE_CKEDITOR = os.path.exists(os.path.join(PROJECT_PATH, "ckeditor"))

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mydb.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "site_media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "staticfiles")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/staticfiles/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
if not HAVE_GRAPPELLI:
    ADMIN_MEDIA_PREFIX = '/staticfiles/admin/'
else:
    ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "static"),
#    os.path.join(PROJECT_PATH, "ckeditor", "static"), # Optionnal
#    os.path.join(PROJECT_PATH, "grappelli", "static"), # Optionnal
#    os.path.join(PROJECT_PATH, "filebrowser", "static"), # Optionnal
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if not HAVE_GRAPPELLI:
    ADMIN_MEDIA_PREFIX = '/staticfiles/admin/'
else:
    ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '' # Your secret key

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    
    'blog.processor.blog_init',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    #'middleware.StripMiddleware',
    #'ballot.BallotMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates"),
    os.path.join(PROJECT_PATH, "appview", "templates", ),
)

INSTALLED_APPS = (
#    'grappelli', # Comment line if not used
#    'filebrowser', # Comment line if not used
#    'ckeditor', # Comment line if not used
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
#    'django_evolution', # Comment line if not used
    
    'notification',
    'capatcha',
    'blog',
    'utils',
    'appview',
)

# Set this constant to True to disable cache system (default is False)
DONT_USE_CACHE = False

# Use cache only in production
bckend = 'django.core.cache.backends.db.DatabaseCache'
if IS_LOCAL == True or DONT_USE_CACHE == True:
    bckend = 'django.core.cache.backends.dummy.DummyCache'

# Install cache
CACHES = {
    'default': {
        'BACKEND' : bckend,
        'LOCATION': 'cache', # database cache table name
    }
}
    
class BLOG_CONFIG:
    class Templates:
        index =     'blog/index.html'
        post =      'blog/post.html'
        tags =      'blog/tags.html'
        categories ='blog/tags.html'
        month =     'blog/bydate.html'
        year =      'blog/bydate.html'
        search =    'blog/search.html'
        all =       'blog/all.html'
    Download = "downloads"
    
    class EmailTemplates:
        newcommentary = "newcomment"

EMAIL_HOST = ''
EMAIL_USER = ''
EMAIL_PASSWORD = ''

''' Capatcha config '''
class CAPATCHA_CONFIG:
    Download = 'downloads/capatcha'
    temp = 'temp'
CAPATCHA_ROOT = os.path.join(MEDIA_ROOT, CAPATCHA_CONFIG.temp)

# CKEditor Config
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Link', 'Unlink', 'Anchor',
              '-',  'Styles','Format','Font','FontSize',
              '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
              '-', 'SpellChecker', 'Scayt',
              '-', 'Maximize',
            ],
            [      'HorizontalRule',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
            ],
            [
                'Outdent','Indent'
            ],
            [      'Image', 'Flash',
              '-', 'Table', 'HorizontalRule','Smiley','SpecialChar'
            ],
            [ 'About' , ]
        ],
        'width': 1050,
        'height': 600,
        'toolbarCanCollapse': False,
    }
}
CKEDITOR_MEDIA_PREFIX = os.path.join(MEDIA_URL, "ckeditor")
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, "ckeditor")

# Grapelli settings
GRAPPELLI_ADMIN_TITLE = "Your Blog name for admin (change me in settings.py)"
THUMB_DIR = os.path.join(MEDIA_ROOT, "thumb")
THUMB_URL = "/site_media/thumb"

    
# Create all directories at first start
ALL_DIRS = (
    CAPATCHA_ROOT,
    CKEDITOR_UPLOAD_PATH,
    THUMB_DIR
)

for d in ALL_DIRS:
    if not os.path.exists(d):
        os.makedirs(d)

