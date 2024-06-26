"""
Django settings for vsf project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Vars that sets the environment settings

env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('VSF_SECRET_KEY')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'debug_toolbar',
]


INSTALLED_APPS = [
    'apps.vsf_base.apps.VsfBaseConfig',
    'apps.configs.apps.ConfigsConfig',
    'apps.main.users.apps.UsersConfig',
    'apps.main.events.apps.EventsConfig',
    'apps.main.cases.apps.CasesConfig',
    'apps.main.measurements.flags.apps.FlagsConfig',
    'apps.main.measurements.apps.MeasurementsConfig',
    'apps.main.measurements.submeasurements.apps.SubmeasurementsConfig',
    'apps.main.ooni_fp.fp_tables.apps.FpTablesConfig',
    'apps.main.sites.apps.SitesConfig',
    'apps.main.asns.apps.AsnsConfig',
    'apps.main.early_alerts.apps.EarlyAlertsConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.main.public_stats.apps.PublicStatsConfig',
]

API_APPS = [
    'apps.api.asns_api.apps.AsnsAPIConfig',
    'apps.api.fp_tables_api.apps.FpTablesAPIConfig',
    'apps.api.public_stats_api.apps.PublicStatsApiConfig',
    'apps.api.cases_api.apps.CasesAPIConfig',
    'apps.api.events_api.apps.EventsAPIConfig',
    'apps.api.measurements_api.apps.MeasurementsAPIConfig',

]

THIRD_PARTY_APPS = [
    'django_prometheus',
    'widget_tweaks',
    'drf_yasg',
    'django_celery_results',
    'django_sass',
    'ckeditor',
    'django_wysiwyg',
    'django_extensions'
]

INSTALLED_APPS = INSTALLED_APPS + DJANGO_APPS + API_APPS + THIRD_PARTY_APPS

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", "http://coruscant.estarguars.org"
]

INTERNAL_IPS = [
    '127.0.0.1',
    env.str('VSF_PRODUCTION_HOST1'), 
    env.str('VSF_PRODUCTION_HOST2'), 
    env.str('VSF_PRODUCTION_HOST3')
]

ROOT_URLCONF = 'vsf.urls'

LOGIN_REDIRECT_URL = "dashboard"   # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "dashboard"  # Route defined in app/urls.py
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/dashboard')],
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

WSGI_APPLICATION = 'vsf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str( 'SQL_ENGINE'),
        'NAME': env.str('VSF_DB_NAME'),
        'USER': env.str('VSF_DB_USER'),
        'PASSWORD': env.str('VSF_DB_PASSWORD'),
        'HOST': env.str('VSF_DB_HOST'),
        'PORT': env.str('VSF_DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Authentication
# --------------------------------------------------

LOGIN_URL = "/dashboard/login"

LOGIN_REDIRECT_URL = "/dashboard"

LOGOUT_REDIRECT_URL = LOGIN_URL

# EMAIL
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST    = env.str("EMAIL_HOST")
# EMAIL_HOST_USER = env.str('VSF_EMAIL_HOST_USER') # email sender user
# EMAIL_HOST_PASSWORD = env.str('VSF_EMAIL_HOST_PASSWORD') # user password
# EMAIL_PORT = env.str("EMAIL_PORT")
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# Prometheus monitor config
PROMETHEUS_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 25.0, 50.0, 75.0, float("inf"),)
PROMETHEUS_LATENCY_BUCKETS = (.1, .2, .5, .6, .8, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.5, 9.0, 12.0, 15.0, 20.0, 30.0, float("inf"))
PROMETHEUS_EXPORT_MIGRATIONS = False

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_TRUSTED_ORIGINS = origins.split(" ") if (origins := env("CSRF_TRUSTED_ORIGINS", default="")) else [] # type: ignore

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'static'),
)

CKEDITOR_BASEPATH = BASE_DIR + STATIC_URL + '/plugins/ckeditor'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379") # type: ignore

# Caching config:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'process_state',
        'TIMEOUT' : 86400
    },
    'filesystem' : {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# Url for the ooni api to get a set of measurements
OONI_MEASUREMENTS_URL = "https://api.ooni.io/api/v1/measurements"

def custom_show_toolbar(request):
    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'