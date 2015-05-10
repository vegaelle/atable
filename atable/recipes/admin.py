from django.contrib import admin
from .models import (Diet, Ingredient, Meal, Recipe, Session, Ustensil,
                     MealParticipant, RecipeIngredient)

admin.site.register(Diet)
admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Session)
admin.site.register(Ustensil)
admin.site.register(MealParticipant)
admin.site.register(RecipeIngredient)
