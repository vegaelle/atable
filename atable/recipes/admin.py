from django.contrib import admin
from django.shortcuts import render
from .models import (Diet, Ingredient, Meal, Recipe, Session, Ustensil,
                     MealParticipant, RecipeIngredient, SessionMeal)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class MealParticipantInline(admin.TabularInline):
    model = MealParticipant


class SessionMealInline(admin.TabularInline):
    model = SessionMeal


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'diets', 'price')
    inlines = [RecipeIngredientInline, ]


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    def generate_roadsheet(modeladmin, request, queryset):
        return render(request, 'recipes/roadsheet_meal.html', {})

    generate_roadsheet.short_description = 'Générer la feuille de route'

    actions = [generate_roadsheet]
    filter_horizontal = ('recipes',)
    inlines = [MealParticipantInline, ]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def generate_roadsheet(modeladmin, request, queryset):
        return render(request, 'recipes/roadsheet_session.html', {})

    generate_roadsheet.short_description = 'Générer la feuille de route'

    actions = [generate_roadsheet]
    inlines = [SessionMealInline, ]


admin.site.register(Diet)
admin.site.register(Ingredient)
admin.site.register(Ustensil)
admin.site.register(MealParticipant)
admin.site.register(RecipeIngredient)
admin.site.register(SessionMeal)
