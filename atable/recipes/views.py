from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView
from .models import Meal, Session, Recipe, RecipeIngredient, Ingredient

class RecipeListView(ListView):
    model = Recipe


class RecipeDetailView(DetailView):
    model = Recipe


@permission_required('meal.can_view')
def roadmap_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    return render(request, 'recipes/roadmap_meal.html', {'meal': meal})


@permission_required('session.can_view')
def roadmap_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, 'recipes/roadmap_session.html',
                  {'session': session})