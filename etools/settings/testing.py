from .base import *

PCS_DATABASE = {
    'HOST': '10.194.12.80',
    'PORT': '5432',
    'USER': 'pcs_view',
    'PWD': 'pcs',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'etools',
        'USER': 'puser',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
