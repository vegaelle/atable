from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Meal


@permission_required('meal.can_generate_roadsheet')
def roadsheet_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    return render(request, 'recipes/roadsheet_meal.html', {'meal': meal})
