# https://docs.djangoproject.com/en/1.9/ref/settings/

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5tb6^d7#d461%g49_hi!k!8*4rj4xef=7_od840=kxxy#j&ana'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'fw_api',
    'fw_common',
    'fw_engine',
    'fw_engine_iptables',
    'fw_engine_puppet'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # '/var/www/static/',
)


WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

import mongoengine
DATABASES = {
    # 'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')},
    'default': {'ENGINE': ''}
}

MONGODB_NAME = 'iptables'
MONGODB_DATABASE_HOST = 'mongodb://iptables:iptables_pass@localhost/%s' % MONGODB_NAME
mongoengine.connect(MONGODB_NAME, host=MONGODB_DATABASE_HOST)


TEST_RUNNER = 'fw_common.testrunner.NoSQLTestRunner'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
