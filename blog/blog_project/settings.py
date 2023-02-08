"""
Django settings for blog_project project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from environs import Env


env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-eb7vni6s1ax7gltgvr$as%$7^8e5vgw=*_x#$-ezuhn9i6!psa'
SECRET_KEY = env.str("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True # development
DEBUG = env.bool("DEBUG", default=False) # production

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "igork.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # serve static files in production
    'django.contrib.staticfiles',
    'taggit',
    'blog_app',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

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

WSGI_APPLICATION = 'blog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": env.dj_db_url("DATABASE_URL")
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_TZ = True
USE_TZ = False
# https://docs.djangoproject.com/en/3.2/ref/utils/#module-django.utils.timezone
# https://www.reddit.com/r/django/comments/p7qhvk/why_is_djangoutilstimezonenowtzinfo_returning_utc/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# NOTE: since Django won’t serve static files in production, we need a few extra steps. The first change is to use Django’s collectstatic command which compiles all static files throughout the project into a single directory suitable for deployment. Second, we must set the STATIC_ROOT configuration, which is the absolute location of these collected files, to a folder called staticfiles. And third, we need to set STATICFILES_STORAGE, which is the file storage engine used by collectstatic.

STATIC_URL = 'static/'
STATICFILES_DIRS = ('static',)
STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Log in/out

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'


# Media
MEDIA_URL = '/media/' # absolute filesystem path to the directory for user-uploaded files
MEDIA_ROOT = BASE_DIR / 'media' # URL we can use in our templates for the files
# https://learndjango.com/tutorials/django-file-and-image-uploads-tutorial


# *** SECURITY ***

# CSRF protection
CSRF_COOKIE_SECURE = True # to avoid transmitting the CSRF cookie over HTTP accidentally
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True # to avoid transmitting the session cookie over HTTP accidentally
# XSS protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SSL Redirect
SECURE_SSL_REDIRECT = True # to force Django redirect all non-HTTPS requests to HTTPS

X_FRAME_OPTIONS = 'DENY'

# HTTP Strict Transport Security
# When this policy is set, browsers will refuse to connect to your site for the given time period if you’re not properly serving HTTPS resources, or if your certificate expires.
SECURE_HSTS_SECONDS = 86400 # 1 day - set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# https://stackoverflow.com/questions/52405589/how-to-check-django-security-vulnerabilities-and-how-to-fix-them
# https://dev.to/thepylot/django-web-security-checklist-before-deployment-secure-your-django-app-4jb8

# RESET SECUTIRY - if Error "You're accessing the development server over HTTPS, but it only supports HTTP" - uncomment the following code
# https://stackoverflow.com/questions/35536491/error-youre-accessing-the-development-server-over-https-but-it-only-supports
# CORS_REPLACE_HTTPS_REFERER = False
# HOST_SCHEME = "http://"
# SECURE_PROXY_SSL_HEADER = None
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = None
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_FRAME_DENY = False

# Pythonanywhere.com deployment:
# https://youtu.be/xtnUwvjOThg
