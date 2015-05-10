from django.db import models


class Diet(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    price = models.FloatField()
    providers = models.TextField()
    diets = models.ManyToManyField(Diet)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey('Recipe')
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.IntegerField()


class Ustensil(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=10,
                                 choices=(('meal', 'Meal'),
                                          ('dessert', 'Dessert'))
                                 )
    parts = models.IntegerField()
    picture = models.ImageField(upload_to='recipe')
    preparation_time = models.DurationField(null=True, blank=True)
    cooking_time = models.DurationField(null=True, blank=True)
    description = models.TextField()
    licence = models.TextField()
    author = models.CharField(max_length=100)
    parent_recipes = models.ManyToManyField('self', blank=True)
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)
    ustensils = models.ManyToManyField(Ustensil, blank=True)

    def __str__(self):
        return self.name


class MealParticipant(models.Model):

    diet = models.ForeignKey('Diet')
    count = models.IntegerField()


class Meal(models.Model):

    name = models.CharField(max_length=100)
    begin = models.TimeField()
    end = models.TimeField()
    recipes = models.ManyToManyField(Recipe)
    participants = models.ManyToManyField(MealParticipant, blank=True)

    def __str__(self):
        return self.name


class SessionMeal(models.Model):

    session = models.ForeignKey('Session')
    meal = models.ForeignKey(Meal)
    date = models.DateField()


class Session(models.Model):

    name = models.CharField(max_length=100)
    meals = models.ManyToManyField(Meal, through=SessionMeal)

    def __str__(self):
        return self.name
