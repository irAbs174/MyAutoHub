"""Local development settings."""

from .base import *  # noqa: F401,F403

DEBUG = True

# SQLite fallback when Postgres is unavailable (optional local convenience)
import os

if os.environ.get("USE_SQLITE", "").lower() in ("1", "true", "yes"):
    DATABASES = {  # noqa: F405
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
