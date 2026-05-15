from .base import *
import os, dj_database_url

SECRET_KEY = 'django-insecure-x#n!z1v!b=vnrsy*r&*)!_4z5dc2qxe)mii*b5g!w4l-ov=^v+'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES = {'default': dj_database_url.config(default=database_url)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }