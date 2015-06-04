from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Ingredient, RecipeIngredient


@receiver(m2m_changed, sender=Ingredient.diets.through)
def pre_save_ingredient(sender, **kwargs):
    """re-checking all meals that include this ingredient to update diets list.
    """
    for recipe in kwargs['instance'].recipe_set.all():
        recipe.get_diets()


@receiver(post_save, sender=RecipeIngredient)
def pre_save_recipe_ingredient(sender, **kwargs):
    """re-fetching the diets for that recipe.
    """
    kwargs['instance'].recipe.get_diets()
