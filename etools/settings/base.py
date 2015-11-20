import sys
from os.path import join, abspath, dirname
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# PATH vars

here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

sys.path.insert(0, root('apps'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE THIS!!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3_datetime',
    'widget_tweaks',
)

PROJECT_APPS = (
    'debug_toolbar',
    'uptime',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'etools.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'etools.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'etools',
        'USER': 'postres',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Omsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = root('assets', 'uploads')

MEDIA_URL = '/media/'

# Additional locations of static files

STATICFILES_DIRS = (
    root('assets'),
)

TEMPLATE_DIRS = (
    root('templates'),
)

DATE_FORMAT = 'd.m.Y'

TIME_FORMAT = 'H:i'

SHORT_DATETIME_FORMAT = 'd.m.Y H:i'

DATE_INPUT_FORMATS = ('%d.%m.%Y')

TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
)

DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M:%S',
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y',
)

LOGIN_URL = '/login/'

STATIC_ROOT = join(PROJECT_ROOT, 'static')

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary
if len(sys.argv) > 1 and 'test' in sys.argv[1]:
    from .testing import *
