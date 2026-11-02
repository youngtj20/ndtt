import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ppymv(p@+dsa8so*t*&!b5!i(l=+6@xzv10!*a@_um!a3^(*x^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',')]

# CORS_ORIGIN_ALLOW_ALL=True
# Application definition

INSTALLED_APPS = [
    'exam',
    'custom',
    'question_bank',
    'welcome',
    'sync',
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'api.middleware.CustomCorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'ndtt.urls'

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
                'ndtt.context_processors.extra_context',
                'ndtt.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'ndtt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


if os.environ.get('APP_ENV', 'DEVELOPMENT') == "PRODUCTION":
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_BACKEND', 'django.db.backends.mysql'),
            'NAME': os.environ.get('DATABASE_NAME', 'ndtt'),
            'USER': os.environ.get('DATABASE_USER', 'root'),
            'PASSWORD': os.environ.get('DATABASE_PASS', ''),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': os.environ.get('DATABASE_PORT', '3306'),
            'CONN_MAX_AGE': 60,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME', 'ndtt'),
            'USER': os.environ.get('DATABASE_USER', 'root'),
            'PASSWORD': os.environ.get('DATABASE_PASS', ''),
            'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DATABASE_PORT', '3306'),
            'CONN_MAX_AGE': 60,
            'OPTIONS': {
                "init_command": "SET foreign_key_checks = 0;",
            },
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': 'mydatabase',
    #     }
    # }

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_LEVEL = 10  # DEBUG
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if os.environ.get('APP_ENV', 'DEVELOPMENT') == "PRODUCTION":
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'auth.User'

LOGIN_URL = '/ap/login/'

MIDDLEWARE += ('crum.CurrentRequestUserMiddleware',)

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    )
}


DATETIME_INPUT_FORMAT = [
    '%m/%d/%Y %H:%M %p',     # '10/25/2006 14:30 PM'
    '%m/%d/%Y %H:%M %p',
    '%m/%d/%Y %H:%M %p',
    '%d/%m/%Y %H:%M %p',
]

DATE_INPUT_FORMAT = [
    '%d/%m/%Y', '%d/%m/%Y',
    '%Y-%m-%d', '%m/%d/%Y',             # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
]

REMOTE_URL = "https://test.ndtt.ng/synchro/"
