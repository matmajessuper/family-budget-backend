import os
from .common import *


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


# Site
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
INSTALLED_APPS += ('gunicorn', )

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [] # TODO change to frontend

