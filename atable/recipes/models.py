from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from .decorators import method_cache


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

    @method_cache()
    def diets_str(self):
        return ', '.join([d.name.title() for d in self.diets.all()]) if\
            self.diets.count() else 'Omnivore'
    diets_str.short_description = 'Régimes'

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
    picture = models.ImageField(upload_to='recipe', verbose_name='image',
                                blank=True)
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

    @method_cache()
    def diets(self):
        """ return the list of diets for this recipe as a comma-separated
        string.
        """
        # TODO: rewrite this heavy shit
        diets = [[d for d in i.diets.all()]
                 for i in self.ingredients.all()]
        total_diets = set()
        for diet in diets:
            if len(total_diets) == 0:
                total_diets = set(diet)
            total_diets = total_diets.intersection(diet)
        return total_diets

    def diets_str(self):
        diets = [d.name for d in self.diets()]
        return ', '.join(diets) if diets else 'Omnivore'
    diets_str.short_description = 'régimes'

    @method_cache()
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

    def diet_name(self):
        return self.diet.name if self.diet else 'Omnivore'

    @method_cache()
    def can_eat(self):
        """returns a list of recipes that those participants can eat.
        """
        if self.diet is None:
            return self.meal.recipes.all()
        return [r for r in self.meal.recipes.all()
                if self.diet in r.diets()]

    def __str__(self):
        return '{meal} — {count} × {diet}'.format(meal=self.meal,
                                                  count=self.count,
                                                  diet=self.diet_name())

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

    @method_cache()
    def recipes_list(self):
        return self.recipes.order_by('meal_type')

    @method_cache()
    def participants(self):
        return self.mealparticipant_set.all()

    @method_cache()
    def participants_count(self):
        return sum([mp.count for mp in self.mealparticipant_set.all()])
    participants_count.short_description = 'Nombre de participants'

    @method_cache()
    def ingredients_list(self):
        """returns a list of ingredients needed for all recipes in this meal.
        The ingredients are returned as dicts containing the Ingredient itself,
        the quantity needed, and the total price of that ingredient.
        """
        ingredients = {}
        for recipe in self.recipes.all():
            for recipe_ingredient in recipe.recipeingredient_set.all():
                if recipe_ingredient.ingredient not in ingredients:
                    ingredients[recipe_ingredient.ingredient] = 0
                ingredients[recipe_ingredient.ingredient] += \
                    recipe_ingredient.quantity

        ingredients_list = []
        for ingredient, quantity in ingredients.items():
            ingredients_list.append({'ingredient': ingredient,
                                     'quantity': quantity,
                                     'price': quantity * ingredient.price})
        return ingredients_list

    @method_cache()
    def total_price(self):
        """returns the sum of the individual price of each ingredient in each
        recipe of the meal.
        """
        price = 0
        for recipe in self.recipes.all():
            for recipe_ingredient in recipe.recipeingredient_set.all():
                price += recipe_ingredient.ingredient.price *\
                    recipe_ingredient.quantity
        return price

    @method_cache()
    def ustensils_list(self):
        ustensils = {}
        for recipe in self.recipes.all():
            for ustensil in recipe.ustensils.all():
                if ustensil not in ustensils:
                    ustensils[ustensil] = []
                ustensils[ustensil].append(recipe)
        return [{'ustensil': u, 'used_in': r} for u, r in ustensils.items()]

    @method_cache()
    def recipe_diet_participants(self):
        """returns a dict containing participants count for each recipe of the
        meal.
        """
        participants = {}
        omni_participants_count = sum([p.count for p in
                                       self.mealparticipant_set
                                       .filter(diet=None)])
        for recipe in self.recipes.all():
            if recipe not in participants:
                participants[recipe] = omni_participants_count
            diets = recipe.diets()
            for diet in diets:
                participants[recipe] += sum([p.count for p in
                                             self.mealparticipant_set
                                             .filter(diet__name=diet)])
        return participants

    def admin_roadsheet(self):
        return '<a href="{url}" title="Générer la feuille de route" '\
               'target="_BLANK"><img src="/static/open-iconic/spreadsheet'\
               '.svg" alt="Générer la feuille de route" /></a>'.format(
                   url=resolve_url('roadsheet_meal',
                                   meal_id=self.id))
    admin_roadsheet.short_description = 'Feuille de route'
    admin_roadsheet.allow_tags = True

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
