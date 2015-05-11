from django.contrib import admin
from .models import (Diet, Ingredient, Meal, Recipe, Session, Ustensil,
                     MealParticipant, RecipeIngredient, SessionMeal)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'diets', 'price')

admin.site.register(Diet)
admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(Session)
admin.site.register(Ustensil)
admin.site.register(MealParticipant)
admin.site.register(RecipeIngredient)
admin.site.register(SessionMeal)
