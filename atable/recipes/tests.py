from django.test import TestCase
from .models import Meal


class MealTest(TestCase):
    fixtures = ['tests']

    def test_meal_participants(self):
        m = Meal.objects.get(pk=1)
        p = m.recipe_diet_participants()
        r1 = m.recipes.get(name='veggie recipe 1')
        r2 = m.recipes.get(name='omni recipe 1')
        self.assertEqual(15, p[r1])
        self.assertEqual(10, p[r2])
