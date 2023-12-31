"""
Django settings for PagesaApp project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ssqi5nt87rk^+*bdxsi)m=j#i#9d$6ev^u20a^3y720ph=_&f$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


CSRF_TRUSTED_ORIGINS = ['https://*.wrbr.xyz']


CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 31536000

LOGIN_URL = 'login-user'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'Stores',
    'storages',
]

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

ROOT_URLCONF = 'PagesaApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Stores.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'PagesaApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tester_db',
        'USER': 'dili_tester',
        'PASSWORD': 'flakerqsxokm1902',
        'HOST': 'database-1.cfjxkc5s0xqx.eu-north-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wriber032@gmail.com'
EMAIL_HOST_PASSWORD = 'bymfvhtmjxbwilij'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_RECIEVER = 'nwosuedward6@gmail.com'
EMAIL_RECIEVER_ALEX = 'chinonsoalexjr@gmail.com'
EMAIL_RECIEVER_EMEKA = 'krypticagha@gmail.com'


#s3 Buckets configs

load_dotenv()

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID = 'AKIAY2TFGLB56SESSPM5'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'wriber-store'

region = 'eu-north-1'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_SIGNATURE_VERSION = "s3v4"

S3_USE_SIGV4 = True
AWS_QUERYSTRING_AUTH = True

AWS_S3_ENDPOINT_URL: 'https://sts.eu-north-1.amazonaws.com'
AWS_S3_REGION_NAME = 'eu-north-1'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'