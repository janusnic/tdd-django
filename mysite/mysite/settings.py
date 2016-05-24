"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from os import path
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8082'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yrqeo^r-a_!)lubg)@en(zn8a^)=x8*g(6-h@*rv_zd%^@m9tj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_CHARSET = 'utf-8'

# Application definition

INSTALLED_APPS = [
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'mptt',
    'ckeditor',
    #'pipeline',
    'ckeditor_uploader',
    'tinymce',
    'shop',
    'userprofiles',
    'bootstrap3',
    'reviews',
    'pages',
    'home',
    'fts',
    'polls',
    'gallery',
    
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #'mysite.assets.CompileAssetsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                
                'shop.processors.context_processors.cart',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
             
        },
    },
]

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_TWITTER_KEY = 'gTVg6h1fPPK0qyUj2Z7M5lKmW'
SOCIAL_AUTH_TWITTER_SECRET = 'EGNPWNHuYqZ74sK08EtsKwIzA4I5HIbpXhcdeFfe1DainSuApL'

SOCIAL_AUTH_FACEBOOK_KEY = '229179783950067'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e29a1d4c0f20ebf83d4cf08c985e8e43'

# Your access token: Access token
TWITTER_OAUTH_TOKEN = '74156305-bI1Vr3AtcZWa5THY8RPyZQYF8SXhkYDJnM21Hh7X9'
# Your access token: Access token secret
TWITTER_OAUTH_SECRET = 'VTy3S2enJFZGrjv4KRA7FK0TaSK2c9s7iMw8pbqje6eYF'
# OAuth settings: Consumer key
TWITTER_CONSUMER_KEY = 'gTVg6h1fPPK0qyUj2Z7M5lKmW'
# OAuth settings: Consumer secret
TWITTER_CONSUMER_SECRET = 'EGNPWNHuYqZ74sK08EtsKwIzA4I5HIbpXhcdeFfe1DainSuApL'


#Access Token    74156305-OhEDIv0gyHtgkbYxKwQZkDqxIbZeghOQi4CuYnABC
#Access Token Secret R2QuHtjZyJDT3NpjlQqBwhZGLgEvdxNHHTrWDNY6QUqfK

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'auth.User'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _

# uk-UA   Ukrainian

LANGUAGES = (
    ('uk', _('Ukrainian')),
    ('en', _('English')),
    
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

PHOTOS_PER_PAGE = 10

CART_SESSION_ID = 'cart'

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'janusnic@gmail.com'

EMAIL_PORT = 1025

FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT 
FILEBROWSER_MEDIA_URL = MEDIA_URL 
FILEBROWSER_STATIC_ROOT = STATIC_ROOT 
FILEBROWSER_STATIC_URL = STATIC_URL 
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/' 
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/' 


APP_TITLE = 'Janus CMS'

GRAPPELLI_ADMIN_TITLE = APP_TITLE

GRAPPELLI_INDEX_DASHBOARD = 'pages.dashboard.PagesDashboard'

MENU_CHOICES = (
    (0, 'Top'),
    (1, 'Left'),
)

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
}