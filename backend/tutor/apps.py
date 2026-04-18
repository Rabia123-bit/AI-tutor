from django.apps import AppConfig
import os

class TutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutor'

    def ready(self):
        from django.contrib.auth.models import User

        if os.environ.get("CREATE_SUPERUSER", "False") == "True":
            username = "admin"
            email = "admin@example.com"
            password = "admin123"

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
