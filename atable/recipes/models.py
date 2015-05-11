from django.db import models
from django.conf import settings


class Diet(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'régime'


class Ingredient(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    unit = models.CharField(max_length=100, verbose_name='unité')
    price = models.FloatField(verbose_name='prix')
    providers = models.TextField(blank=True, verbose_name='fournisseurs')
    diets = models.ManyToManyField(Diet, blank=True, verbose_name='régimes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ingrédient'


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey('Recipe', verbose_name='recette')
    ingredient = models.ForeignKey(Ingredient, verbose_name='ingrédient')
    quantity = models.IntegerField(verbose_name='quantité')

    def __str__(self):
        return '{recipe} — {ingredient}'.format(recipe=self.recipe,
                                                ingredient=self.ingredient)

    class Meta:
        verbose_name = 'ingrédient de recette'
        verbose_name_plural = 'ingrédients de recette'


class Ustensil(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ustensile'


class Recipe(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    meal_type = models.CharField(max_length=10,
                                 choices=(('meal', 'plat'),
                                          ('dessert', 'dessert')),
                                 verbose_name='type de recette',
                                 )
    parts = models.IntegerField(verbose_name='nombre de parts')
    picture = models.ImageField(upload_to='recipe', verbose_name='image')
    preparation_time = models.DurationField(null=True, blank=True,
                                            verbose_name='temps de '
                                            'préparation',
                                            help_text='Entrez le temps de '
                                            'préparation requis, au format '
                                            'HH:MM:SS. Laissez vide si non '
                                            'nécessaire.')
    cooking_time = models.DurationField(null=True, blank=True,
                                        verbose_name='temps de cuisson',
                                        help_text='Entrez le temps de '
                                        'cuisson requis, au format HH:MM:SS. '
                                        'Laissez vide si non nécessaire.')
    description = models.TextField(verbose_name='descriptif de la recette')
    licence = models.TextField(blank=True, verbose_name='licence',
                               default=settings.DEFAULT_RECIPE_LICENCE)
    author = models.CharField(max_length=100, verbose_name='auteur',
                              default=settings.DEFAULT_RECIPE_AUTHOR)
    parent_recipes = models.ManyToManyField('self', blank=True,
                                            verbose_name='recettes parentes')
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient,
                                         verbose_name='ingrédients')
    ustensils = models.ManyToManyField(Ustensil, blank=True,
                                       verbose_name='ustensiles')

    def __str__(self):
        return self.name

    def diets(self):
        """ return the list of diets for this recipe as a comma-separated
        string.
        """
        diets = [[str(d) for d in i.diets.all()]
                 for i in self.ingredients.all()]
        total_diets = set()
        for diet in diets:
            if len(total_diets) == 0:
                total_diets = set(diet)
            total_diets = total_diets.intersection(diet)
        return ', '.join(total_diets)
    diets.short_description = 'régimes'

    def price(self):
        """ return the total price of the recipe
        """
        price = 0
        for recipe_ingredient in self.recipeingredient_set.all():
            price += recipe_ingredient.ingredient.price *\
                recipe_ingredient.quantity
        return '{} €'.format(price)  # TODO: the currency should be dynamic
    price.short_description = 'prix'

    class Meta:
        verbose_name = 'recette'


class MealParticipant(models.Model):

    meal = models.ForeignKey('Meal', verbose_name='repas')
    diet = models.ForeignKey(Diet, verbose_name='régime', blank=True,
                             null=True,
                             help_text='Laissez vide si pas de régime spécial')
    count = models.IntegerField(verbose_name='nombre de personnes')

    def __str__(self):
        return '{session} — {count} × {diet}'.format(session=self.meal,
                                                     count=self.count,
                                                     diet=self.diet)

    class Meta:
        verbose_name = 'participant à un repas'
        verbose_name_plural = 'participants à un repas'


class Meal(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    begin = models.TimeField(verbose_name='heure de début',
                             help_text='Entrez l’heure de début, au format '
                             'HH:MM:SS')
    end = models.TimeField(verbose_name='heure de fin',
                           help_text='Entrez l’heure de fin, au format '
                           'HH:MM:SS')
    recipes = models.ManyToManyField(Recipe, verbose_name='recettes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'repas'
        verbose_name_plural = 'repas'


class SessionMeal(models.Model):

    session = models.ForeignKey('Session', verbose_name='session')
    meal = models.ForeignKey(Meal, verbose_name='repas')
    date = models.DateField(verbose_name='date')

    def __str__(self):
        return '[{date}] {meal} pour {session}'.format(
            date=self.date.strftime(settings.DEFAULT_DATE_FORMAT),
            meal=self.meal,
            session=self.session)

    class Meta:
        verbose_name = 'repas de session'
        verbose_name_plural = 'repas de session'


class Session(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    meals = models.ManyToManyField(Meal, through=SessionMeal,
                                   verbose_name='repas')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'session'
