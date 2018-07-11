from .base import *

SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
