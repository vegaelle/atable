from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Ingredient


@receiver(m2m_changed, sender=Ingredient.diets.through)
def pre_save_ingredient(sender, **kwargs):
    """re-checking all meals that include this ingredient to update diets list.
    """
    for recipe in kwargs['instance'].recipe_set.all():
        recipe.get_diets()
        recipe.save()
