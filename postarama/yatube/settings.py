"""
Django settings for yatube project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from distutils.util import strtobool

import sentry_sdk
from django.contrib import messages
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG_VALUE"))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    "my_users",
    "posts",
    "django.contrib.flatpages",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.sites",
    "sorl.thumbnail",
    "debug_toolbar",
    "markdownx",
    "taggit",
    "likes",
    "bookmarks",
    "django.contrib.postgres",
    "bootstrap4",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.vk",
    "pytils",
    "django_extensions",
    "feedback",
    "about",
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "vk": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": os.getenv("VK_CLIENT_ID"),
            "secret": os.getenv("VK_SECRET"),
            "key": os.getenv("VK_KEY"),
        }
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "yatube.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "posts.views.year",
            ],
        },
    },
]

WSGI_APPLICATION = "yatube.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

TEMPLATE_DIRS = ["static"]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

# Login
LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "follow_index"

SITE_ID = 1

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TO = [os.getenv("EMAIL_TO")]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
os.environ["HTTPS"] = "on"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

MARKDOWNX_UPLOAD_MAX_SIZE = 50 * 2048 * 2048
MARKDOWNX_IMAGE_MAX_SIZE = {"size": (960, 960), "quality": 90}

TAGGIT_CASE_INSENSITIVE = True
CRISPY_TEMPLATE_PACK = "bootstrap4"
