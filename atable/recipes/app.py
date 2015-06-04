from django.apps import AppConfig


class RecipesConfig(AppConfig):
    name = 'recipes'
    verbose_name = 'Gestion de cantine'

    def ready(self):
        from . import signals
