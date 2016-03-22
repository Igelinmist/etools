from .base import *

PCS_DATABASE = {
    'HOST': '10.194.12.80',
    'PORT': '5432',
    'USER': 'pcs_view',
    'PWD': 'pcs',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/django_simple_skeleton_test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
