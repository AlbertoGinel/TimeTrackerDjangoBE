# days/apps.py
from django.apps import AppConfig

class DaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'days'

    def ready(self):
        # Import signals when app is ready
        import days.signals  # noqa