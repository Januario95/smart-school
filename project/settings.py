import os
import pymemcache
from pathlib import Path
from app2.helpers import shuffle, SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-dv89j2#x53lmm9+o0+z448ar@xrabvrus2#@^(j%a0=41se6(i'
SECRET_KEY = shuffle()
# SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 'django.contrib.gis',

    # Internal apps
    # 'app.apps.AppConfig',
    'app2.apps.App2Config',

    # Third-party
    'corsheaders',
    'rest_framework',
    # 'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        # 'ENGINE': 'django.db.backends.mysql',
        # # 'NAME': 'mark_management',
        # 'NAME': 'mark_management2',
        # 'USER': 'root',
        # 'PASSWORD': 'Young1995@',
        # 'HOST': 'localhost',
        # 'PORT': 3306
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient'
#         }
#     }
# }

# CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
    #     'LOCATION': '127.0.0.1:11211'
    # }
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
    #     'LOCATION': 'unix:/temp/memcached.sock'
    # },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
    #     'LOCATION': [
    #         '172.19.26.240:11211',
    #         '172.19.26.242:11212',
    #         '172.19.26.244:11213'
    #     ],
    #     'OPTIONS': {
    #         'allow_unicode_keys': True,
    #         'default_noreply': False,
    #         'serde': pymemcache.serde.pickle_serde
    #     }
    # }
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.redis.RedisCache',
    #     # 'LOCATION': 'redis://127.0.0.1:6379',
    #     # 'LOCATION': 'redis://januario92:Jaci1995@127.0.0.1:6379',
    #     'LOCATION': [
    #         'redis://127.0.0.1:6379',  # leader
    #         'redis://127.0.0.1:6378',  # read-replica 1
    #         'redis://127.0.0.1:6377',  # read-replica 2
    #     ]
    # }
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'my_cache_table'
    # }
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     # 'LOCATION': '/var/tmp/django_cache'
    #     'LOCATION': 'C:/Users/a248433/Documents/Practice/Programming/My Projects/MarksManagement/first/cache'
    # }
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 11,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-US'
LANGUAGE_CODE = 'pt-Br'

TIME_ZONE = 'Africa/Maputo'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

LOGIN_URL = '/entrar/'
# LOGIN_REDIRECT_URL = '/lista_de_estudantes/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SESSION_COOKIE_AGE = 1209600 # DEFAULT SESSION AGE OF 2 WEEKS
# SESSION_COOKIE_SECURE = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
]


def show_toolbar(request):
    return True

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': show_toolbar
# }

# When using Per-Site Caching
# CACHE_MIDDLEWARE_ALIAS  = ' ' # cache alias
# CACHE_MIDDLEWARE_SECONDS = 600 # number of seconds each page should be cached.
# CACHE_MIDDLEWARE_KEY_PREFIX = ''  # name of site if multiple sites are used