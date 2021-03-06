"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(2u$1!tpv3kgxk5_1#hf2^330-4&!-*^9@rj3l%oz@vrc(7^(_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'markdownx',
)
#    'markdown_deux',
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
LOGIN_REDIRECT_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'  # my gmail password
EMAIL_HOST_USER = 'django.mails@gmail.com'  # my gmail username
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
]

# Markdownify
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'  # Default function that compiles markdown using defined extensions. Using custom function can allow you to pre-process or post-process markdown text. See below for more info.

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = []  # List of used markdown extensions. See below for more info.
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {}  # Configuration object for used markdown extensions

# Markdown urls
MARKDOWNX_URLS_PATH = '/markdownx/markdownify/'  # URL that returns compiled markdown text.
MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/'  # URL that accepts file uploads, returns markdown notation of the image.

# Media path
MARKDOWNX_MEDIA_PATH = 'markdownx/'  # Path, where images will be stored in MEDIA_ROOT folder

# Image
MARKDOWNX_UPLOAD_MAX_SIZE = 52428800  # 50MB - maximum file size
MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png']  # Acceptable file content types
MARKDOWNX_IMAGE_MAX_SIZE = {'size': (500, 500), 'quality': 90}  # Different options describing final image processing: size, compression etc. See below for more info.

# Editor
MARKDOWNX_EDITOR_RESIZABLE = True  # Update editor's height to inner content height while typing
