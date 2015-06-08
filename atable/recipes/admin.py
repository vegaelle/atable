from django.contrib import admin
from django import forms
from sorl.thumbnail.admin import AdminImageMixin
from .models import (Diet, Ingredient, Meal, Recipe, Session, Ustensil,
                     MealParticipant, RecipeIngredient, ParentRecipe)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class MealParticipantInline(admin.TabularInline):
    model = MealParticipant


class SessionMealInline(admin.TabularInline):
    model = Meal


class ParentRecipeInline(admin.TabularInline):
    model = ParentRecipe
    fk_name = 'child'
    extra = 1


class DietIngredientsForm(forms.ModelForm):
    ingredients = forms\
        .ModelMultipleChoiceField(label='Ingrédients',
                                  queryset=Ingredient.objects.all(),
                                  required=False,
                                  help_text='Sélectionnez les ingrédients '
                                            'compatibles',
                                  widget=admin.widgets
                                  .FilteredSelectMultiple('ingredients',
                                                          False)
                                  )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'diets_str')
    exclude = ['diets']
    list_filter = ('diets__name',)
    search_fields = ['name', 'diets__name']


@admin.register(Recipe)
class RecipeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'diets_str', 'price', 'meal_type', 'parts',
                    'picture_str')
    filter_horizontal = ('ustensils',)
    exclude = ['diets']
    inlines = [RecipeIngredientInline, ParentRecipeInline]
    list_filter = ('diets__name', 'meal_type')
    search_fields = ['name', 'meal_type', 'diets__name', 'description']


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipes',)
    inlines = [MealParticipantInline, ]
    list_display = ('name', 'participants_count', 'date',
                    'admin_roadmap')
    search_fields = ['name', 'recipes__name']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_roadmap')
    inlines = [SessionMealInline]


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    form = DietIngredientsForm

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['ingredients'].initial = \
                [o.pk for o in obj.ingredient_set.all()]
        else:
            self.form.base_fields['ingredients'].initial = []
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.ingredient_set.clear()
        for ingredient in form.cleaned_data['ingredients']:
            obj.ingredient_set.add(ingredient)


admin.site.register(Ustensil)
# admin.site.register(MealParticipant)
# admin.site.register(RecipeIngredient)
