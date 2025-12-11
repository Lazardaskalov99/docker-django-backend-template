from pathlib import Path
from decouple import config
from kombu import Queue
from datetime import timedelta


# -----------------------------------------------------
# Paths
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------
# Security / Core
# -----------------------------------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="change-me-in-prod")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

USE_X_FORWARDED_HOST = config("DJANGO_USE_X_FORWARDED_HOST", default=False, cast=bool)

_secure_proxy = config("DJANGO_SECURE_PROXY_SSL_HEADER", default=None)
if _secure_proxy:
    name, val = _secure_proxy.split(",", 1)
    SECURE_PROXY_SSL_HEADER = (name.strip(), val.strip())


# -----------------------------------------------------
# Static & Media
# -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------
# Hosts (override in dev/prod)
# -----------------------------------------------------
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="*", cast=lambda v: v.split(","))
CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED", default="http://127.0.0.1", cast=lambda v: v.split(","))


# -----------------------------------------------------
# Installed Apps
# -----------------------------------------------------
INSTALLED_APPS = [
    # Project Apps (before Django admin to override templates)
    "apps.admin_panel",
    
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",

    # Third-party
    "modeltranslation",
    "django_filters",
    "behave_django",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "channels",

    # Project Apps 
    "apps.gateway",
]


#AUTH_USER_MODEL = "apps.user_auth.User"


# -----------------------------------------------------
# Middleware
# -----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",

    # Project middleware
    'apps.gateway.middleware.RequestViewerMiddleware',
]


# -----------------------------------------------------
# URLs / WSGI / ASGI
# -----------------------------------------------------
ROOT_URLCONF = "apps.gateway.urls"
ASGI_APPLICATION = "apps.gateway.asgi.application"
WSGI_APPLICATION = "apps.gateway.wsgi.application"


# -----------------------------------------------------
# Templates
# -----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src/admin_service/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]


# -----------------------------------------------------
# Database (PostGIS)
# -----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("DB_Name", default="postgres"),
        "USER": config("DB_User", default="postgres"),
        "PASSWORD": config("DB_Password", default="postgres"),
        "HOST": config("DB_Host", default="db"),
        "PORT": config("DB_Port", default="5432"),
        "TEST": {
            "NAME": "test_database",
        },
    }
}


# -----------------------------------------------------
# Localization
# -----------------------------------------------------
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("it", "Italian"),
    ("de", "German"),
]

USE_TZ = True
TIME_ZONE = "Europe/Berlin"


# -----------------------------------------------------
# CORS / CSRF
# -----------------------------------------------------
CORS_ALLOW_CREDENTIALS = True


# -----------------------------------------------------
# Channels
# -----------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}


# -----------------------------------------------------
# Celery
# -----------------------------------------------------
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

CELERY_TASK_QUEUES = (Queue("default"),)
CELERY_TASK_DEFAULT_QUEUE = "default"


# -----------------------------------------------------
# REST Framework
# -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


# -----------------------------------------------------
# JWT Settings
# -----------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}


# -----------------------------------------------------
# Logging
# -----------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
