from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "demo-only-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ROOT_URLCONF = "wordle.urls"

INSTALLED_APPS = ["django.contrib.staticfiles"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Demo stores games in memory and deliberately has no database configuration.
DATABASES = {}
