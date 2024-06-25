from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'thewalmer.com']


CSRF_TRUSTED_ORIGINS = [
    'https://thewalmer.com',
]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config['POSTGRES_DB'],
        "HOST": config['POSTGRES_HOST'],
        "USER": config['POSTGRES_USER'],
        "PASSWORD": config['POSTGRES_PASSWORD'],
        "PORT": config['POSTGRES_PORT'],
    }
}


# For production, use a real email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config['EMAIL_HOST']
EMAIL_PORT = config['EMAIL_PORT']
EMAIL_USE_TLS = config['EMAIL_USE_TLS']
EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']


# For security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



print("Using settings module:", os.environ.get('DJANGO_SETTINGS_MODULE'))