from .base import *

SECRET_KEY = 'django-insecure-x#n!z1v!b=vnrsy*r&*)!_4z5dc2qxe)mii*b5g!w4l-ov=^v+'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}