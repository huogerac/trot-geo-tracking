import os
from pathlib import Path

import dj_database_url
from decouple import config, Csv
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="geotracking.fly.dev",
    cast=Csv(),
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://geotracking.fly.dev",
    cast=Csv(),
)

# CORS
CORS_ALLOW_CREDENTIALS = config("CORS_ALLOW_CREDENTIALS", default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:3000",
    cast=Csv(),
)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "whitenoise.runserver_nostatic",
]

# CORS
if CORS_ALLOW_CREDENTIALS:
    THIRD_PARTY_APPS += ["corsheaders"]

LOCAL_APPS = [
    "geotracking.base",
    "geotracking.accounts",
    "geotracking.core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS
if CORS_ALLOW_CREDENTIALS:
    before_common = MIDDLEWARE.index("django.middleware.common.CommonMiddleware")
    MIDDLEWARE.insert(before_common, "corsheaders.middleware.CorsMiddleware")

ROOT_URLCONF = "geotracking.geotracking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "geotracking.geotracking.wsgi.application"

AUTH_USER_MODEL = "accounts.User"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASE_URL = config("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = config("LANGUAGE_CODE", default="pt-br")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = config(
    "DJANGO_STATIC_ROOT", default=os.path.join(BASE_DIR.parent, "static")
)

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES = {
    "default": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module}:{lineno} {process:d} {message}",
            "style": "{",
        },
        "console": {
            "format": "{levelname} {asctime} {module}:{lineno} {process:d} {message}",
            "style": "{",
        },
        "django": {
            "format": "{levelname} {asctime} {module}:{lineno} {process:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "django": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "": {
            "level": LOG_LEVEL,
            "handlers": [
                "console",
            ],
        },
        "django.server": {
            "level": LOG_LEVEL,
            "handlers": [
                "console",
            ],
        },
    },
}

# LOGGING = {
#     'version': 1,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.getenv('DJANGO_LOG_FILE', './geotracking.log'),
#             'formatter': 'simple'
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file'],
#             'level': 'DEBUG' if DEBUG else 'INFO',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG' if DEBUG else 'INFO',
#             'propagate': True,
#         },
#     }
# }

# if DEBUG:
#     # make all loggers use the console.
#     for logger in LOGGING['loggers']:
#         LOGGING['loggers'][logger]['handlers'] = ['console']
