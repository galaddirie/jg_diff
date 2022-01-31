"""
Django settings for jg_diff project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta as td
import dj_database_url
import django_on_heroku
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", '12345678910')
RIOT_API_KEY = os.environ.get(
    "RIOT_API_KEY", 'RGAPI-b94771b6-c67d-4a91-8801-23d19baf64fd')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG_VALUE", 'True') == 'True'

ALLOWED_HOSTS = ['https://jg-diff.herokuapp.com/']


# Application definition

INSTALLED_APPS = [
    'summoner.apps.SummonerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'active_link',
    'django_cassiopeia',
]

# os.environ["RIOT_API_KEY"]  # api key in env var
CASSIOPEIA_RIOT_API_KEY = RIOT_API_KEY
CASSIOPEIA_LIMITING_SHARE = 1.0
CASSIOPEIA_DEFAULT_REGION = "NA"   # default region
CASSIOPEIA_LOGGING = {
    "PRINT_CALLS": True,
    "PRINT_RIOT_API_KEY": False,
    "DEFAULT": "WARNING",
    "CORE": "WARNING"
}


CACHES = {
    'default': {  # Do not use it for ALIAS
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    "cass-redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://localhost:6379'),
        "OPTIONS": {
            'PASSWORD': os.environ.get('REDIS_PASSWORD'),
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
        }
    },
    'filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'filebased-cache'),
        'MAX_ENTRIES': 10000,
    }
}


CASSIOPEIA_PIPELINE = {
    "Omnistone": {
        "EXPIRATIONS_MAP": {
            td(hours=3): ["c", "c+", "r", "r+", "cr", "i", "i+", "pi", "pi+"],
            td(hours=6): ["rl", "v", "ss", "ss+", "mp", "mp+", "ls", "ls+"],
            0: ["*+"]
        },
        "MAX_ENTRIES": 6000,
        "CULL_FRECUENCY": 2,
        "SAFE_CHECK": True,
        "LOGS_ENABLED": False,
    },
    "DjangoCache": [
        {
            "ALIAS": "cass-redis",
            "EXPIRATIONS_MAP": {
                td(hours=6): ["rl-", "v-", "cr-", "cm-", "cm+-", "cl-", "gl-", "ml-", ],
                td(days=7): ["mp-", "mp+-", "ls-", "ls+-", "t-", 'm-'],
                td(minutes=15): ["cg-", "fg-", "shs-", "s-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": False,
        },
        {
            "ALIAS": "filebased",
            "EXPIRATIONS_MAP": {
                td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": False,
        }
    ],
    "DDragon": {},
    "RiotAPI": {},
}


CASSIOPEIA_API_ERROR_HANDLING = {
    "404": ["t"],
    "500": ["^e", 3, 2, 3],
    "503": ["^e", 3, 2, 3],
    "TIMEOUT": ["^e", 3, 2, 3],
    "403": ["t"],
    "429": {
        "SERVICE": ["^e", 3, 2, 3],
        "METHOD": ["r", 5],
        "APPLICATION": ["r", 5],
    },
}


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

ROOT_URLCONF = 'jg_diff.urls'

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

WSGI_APPLICATION = 'jg_diff.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


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

STATIC_URL = '/static/'

os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Heroku Logging
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
# Heroku settings
django_on_heroku.settings(locals())
# del DATABASES['default']['OPTIONS']['sslmode']
