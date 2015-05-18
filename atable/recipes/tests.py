from django.test import TestCase
from .models import Meal


class MealTest(TestCase):
    fixtures = ['tests']

    def test_meal_participants(self):
        m = Meal.objects.get(pk=1)
        p = m.recipe_diet_participants()
        veggie = m.recipes.get(name='veggie recipe 1')
        omni = m.recipes.get(name='omni recipe 1')
        self.assertEqual(15, p[veggie])
        self.assertEqual(10, p[omni])

    def test_can_eat(self):
        m = Meal.objects.get(pk=1)
        part_omni = m.participants()[0]
        part_veggie = m.participants()[1]
        part_gluten = m.participants()[2]
        recipe_veggie = m.recipes.get(name='veggie recipe 1')
        recipe_omni = m.recipes.get(name='omni recipe 1')

        self.assertIn(recipe_veggie, part_omni.can_eat())
        self.assertIn(recipe_omni, part_omni.can_eat())
        self.assertNotIn(recipe_omni, part_veggie.can_eat())
        self.assertIn(recipe_veggie, part_veggie.can_eat())
        self.assertEqual([], part_gluten.can_eat())

    def test_total_price(self):
        m = Meal.objects.get(pk=1)
        self.assertEqual(212.0, m.total_price())

        m = Meal.objects.get(pk=2)
        self.assertEqual(34.0, m.total_price())
