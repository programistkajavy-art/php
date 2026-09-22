import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wordle.settings")
django.setup()
