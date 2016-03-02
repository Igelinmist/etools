from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/django_simple_skeleton_test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'fdata': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fdata',
        'USER': 'pcs_view',
        'PASSWORD': 'pcs',
        'HOST': '10.194.12.80',
        'PORT': '5432',
    },
}
