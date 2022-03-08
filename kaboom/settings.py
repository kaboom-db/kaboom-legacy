"""
Django settings for kaboom project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from . import db_secrets

# // TODO(#11): Make Kaboom self hostable
# //    This means that sendgrid, aws s3 and pgsql should be optional.
PGSQL = True
SENDGRID = False
AWS_S3 = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r)bhqr+crl4b#^s-=@g!t6cfm8s79-w(m5n44)y#c^fvnaee03'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'comics.apps.ComicsConfig',
    'cartoons.apps.CartoonsConfig',
    'users.apps.UsersConfig',
    'website.apps.WebsiteConfig',
    'social.apps.SocialConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'django_bleach'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kaboom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'kaboom.wsgi.application'

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'index'

if SENDGRID:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    DEFAULT_FROM_EMAIL = db_secrets.DEFAULT_FROM_EMAIL
    EMAIL_HOST = db_secrets.EMAIL_HOST
    EMAIL_HOST_USER = db_secrets.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = db_secrets.SENDGRID_APIKEY
    EMAIL_PORT = db_secrets.EMAIL_PORT
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    DEFAULT_FROM_EMAIL = "kaboom@localhost"
    EMAIL_FILE_PATH = str(BASE_DIR / 'sent_emails')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if PGSQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': db_secrets.DB_NAME,
            'USER': db_secrets.DB_USER,
            'PASSWORD': db_secrets.DB_PASS,
            'HOST': db_secrets.DB_HOST,
            'PORT': db_secrets.DB_PORT
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATICFILES_DIRS = (str(BASE_DIR / "static"),)
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '60/minute'
    }
}

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'center']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style', 'src']
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant'
]
BLEACH_ALLOWED_PROTOCOLS = [
    'http', 'https', 'data'
]
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = False

if AWS_S3:
    AWS_ACCESS_KEY_ID = db_secrets.AWS_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = db_secrets.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = db_secrets.AWS_BUCKET_NAME
    AWS_S3_SIGNATURE_VERSION = db_secrets.AWS_S3_SIGNATURE_VERSION
    AWS_S3_REGION_NAME = db_secrets.AWS_S3_REGION_NAME
    AWS_S3_FILE_OVERWRITE = db_secrets.AWS_S3_FILE_OVERWRITE
    AWS_DEFAULT_ACL = db_secrets.AWS_DEFAULT_ACL
    AWS_S3_VERIFY = db_secrets.AWS_S3_VERIFY
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
    AWS_QUERYSTRING_AUTH = db_secrets.AWS_QUERYSTRING_AUTH
