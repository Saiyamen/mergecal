# ruff: noqa: E501 ERA001
"""Minimal settings for Render.com deployment - no AWS/Sentry/Mailjet required."""

from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["mergecal.onrender.com", "localhost", "127.0.0.1"])

# DATABASES - uses DATABASE_URL env var set by Render
# Already handled in base.py with default

# CACHES - use dummy cache (no Redis required)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Remove health check apps that require Redis/mail connections on startup
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in [
    "health_check.contrib.redis",
    "health_check.contrib.mail",
]]

# SECURITY
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# STATIC & MEDIA - whitenoise for static, local filesystem for media
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# EMAIL - console backend (no external email service needed)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="MergeCal <noreply@mergecal.org>")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# ADMIN URL
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# django-compressor - disable offline compression
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=False)
COMPRESS_OFFLINE = False

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Stripe - use test mode with existing test keys
STRIPE_LIVE_MODE = False
STRIPE_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY", default="sk_test_dummy")
STRIPE_PUBLIC_KEY = env("STRIPE_TEST_PUBLIC_KEY", default="pk_test_dummy")
STRIPE_LIVE_SECRET_KEY = env("STRIPE_LIVE_SECRET_KEY", default="sk_test_dummy")
STRIP_LIVE_PUBLIC_KEY = env("STRIPE_LIVE_PUBLIC_KEY", default="pk_test_dummy")
