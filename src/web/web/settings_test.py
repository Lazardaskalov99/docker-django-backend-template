from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # in-memory SQLite
    }
}

# Disable migrations (faster + avoids DB dependencies)
class DisableMigrations(dict):
    def __contains__(self, item): return True
    def __getitem__(self, item): return None

MIGRATION_MODULES = DisableMigrations()
