from django.apps import AppConfig


class PlannenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "openplan.plannen"

    def ready(self):
        from . import metrics  # noqa
