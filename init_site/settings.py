"""
Django settings for init_site project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # for Heroku
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # for Heroku (along with middleware)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c+xgd_ire-)+-uf1#=6y1678n5j6qs2h%dm1b*5zu*!zuncv3-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("STATUS") != "prod"  # HEROKU Environment Var -> STATUS = prod

ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]  # herokuapp.com for Heroku


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for Heroku
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "init_site.urls"

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

WSGI_APPLICATION = "init_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
if os.environ.get("STATUS") == "prod":  # update for Heroku
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=600, ssl_require=True
    )  # update for Heroku


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "EST"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# vvv Authentication vvv
INSTALLED_APPS += [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]
MIDDLEWARE += [
    "allauth.account.middleware.AccountMiddleware",
]
LOGIN_REDIRECT_URL = "/"
SITE_ID = 1
# Set up under Ryland's Email
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_AUTH_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_AUTH_CLIENT_SECRET"),
            "key": "",
        }
    }
}
# Makes Social Login with without Intermediate Page
SOCIALACCOUNT_LOGIN_ON_GET = True
# ^^^ Authentication ^^^

# vvv Setting New Users vvv
AUTH_USER_MODEL = "main.CustomUser"  # necessarry to change the default user model
# ^^^ Setting New Users ^^^

# vvv Custom Signup Form (Add First and Last Name to Non-Social Signups) vvv
ACCOUNT_FORMS = {
    "signup": "main.forms.CustomSignupForm",
}
# ^^^ Custom Signup Form ^^^

# vvv Email (Fake Email Backend (We Have No Email Server)) vvv
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
# ^^^ Email ^^^

# vvv S3 (Amazon Web Services) vvv
INSTALLED_APPS += ["storages"]

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# ^^^ S3 (Amazon Web Services) ^^^

# Activate Django-Heroku.
# Use this code to avoid the psycopg2 / django-heroku error!
# Do NOT import django-heroku above!
# ty Sherriff :)
try:
    if "HEROKU" in os.environ:
        import django_heroku

        django_heroku.settings(locals())
except ImportError:
    found = False
