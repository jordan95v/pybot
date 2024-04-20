from django.apps import AppConfig

__all__ = ["CoreConfig"]


class CoreConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.core"
