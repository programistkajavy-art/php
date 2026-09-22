import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = "demo-only-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ROOT_URLCONF = "wordle.urls"

INSTALLED_APPS = ["django.contrib.staticfiles", "game"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

azure_sql_settings = {
    "NAME": os.getenv("AZURE_SQL_DATABASE"),
    "USER": os.getenv("AZURE_SQL_USER"),
    "PASSWORD": os.getenv("AZURE_SQL_PASSWORD"),
    "HOST": os.getenv("AZURE_SQL_HOST"),
    "PORT": os.getenv("AZURE_SQL_PORT", "1433"),
}

if all(azure_sql_settings.values()):
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            **azure_sql_settings,
            "OPTIONS": {
                "driver": os.getenv(
                    "AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server"
                )
                #,
                #"extra_params": "Encrypt=yes;TrustServerCertificate=no;",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "local.sqlite3",
        }
    }
