from django.db import models


class Diet(models.Model):

    name = models.CharField(max_length=100)


class Ingredient(models.Model):

    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    price = models.FloatField()
    providers = models.TextField()
    diets = models.ManyToManyField(Diet)


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey('Recipe')
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField()


class Ustensil(models.Model):

    name = models.CharField(max_length=100)


class Recipe(models.Model):

    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=10,
                                 choices=(('meal', 'Meal'),
                                          ('dessert', 'Dessert'))
                                 )
    parts = models.IntegerField()
    picture = models.ImageField(upload_to='recipe')
    preparation_time = models.DurationField()
    cooking_time = models.DurationField()
    description = models.TextField()
    licence = models.TextField()
    author = models.CharField(max_length=100)
    parent_recipes = models.ManyToManyField('self')
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)
    ustensils = models.ManyToManyField(Ustensil)


class MealParticipant(models.Model):

    diet = models.ForeignKey('Diet')
    count = models.IntegerField()


class Meal(models.Model):

    name = models.CharField(max_length=100)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    recipes = models.ManyToManyField(Recipe)
    participants = models.ManyToManyField(MealParticipant)


class SessionMeal(models.Model):

    session = models.ForeignKey('Session')
    meal = models.ForeignKey(Meal)
    date = models.DateField()


class Session(models.Model):

    name = models.CharField(max_length=100)
    meals = models.ManyToManyField(Meal, through=SessionMeal)
