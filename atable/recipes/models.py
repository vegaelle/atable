from collections import OrderedDict
from math import ceil
from datetime import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from calendar import Calendar
from dateutils import relativedelta
from sorl.thumbnail import ImageField, get_thumbnail
from django.template.defaultfilters import pluralize
from .decorators import method_cache


class Diet(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'régime'


class Ingredient(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    unit = models.CharField(max_length=100, verbose_name='unité',
                            choices=(('g', 'g'),
                                     ('kg', 'kg'),
                                     ('cl', 'cl'),
                                     ('l', 'l'),
                                     ('unit', 'unité'),))
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

    def get_absolute_url(self):
        return resolve_url('ingredient_detail', pk=self.pk)

    class Meta:
        verbose_name = 'ingrédient'


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey('Recipe', verbose_name='recette')
    ingredient = models.ForeignKey(Ingredient, verbose_name='ingrédient')
    quantity = models.FloatField(verbose_name='quantité')

    def __str__(self):
        if self.recipe and self.ingredient:
            return '{recipe} — {ingredient}'\
                .format(recipe=self.recipe, ingredient=self.ingredient)
        else:
            return 'Ingrédient de recette'

    class Meta:
        verbose_name = 'ingrédient de recette'
        verbose_name_plural = 'ingrédients de recette'


class Ustensil(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ustensile'


class ParentRecipe(models.Model):
    parent = models.ForeignKey('Recipe', verbose_name='recette parente',
                               related_name='childrecipe_set')
    child = models.ForeignKey('Recipe', verbose_name='recette enfant',
                              related_name='parentrecipe_set')

    class Meta:
        verbose_name = 'recette parente'
        verbose_name_plural = 'recettes parentes'


class Recipe(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    meal_type = models.CharField(max_length=10,
                                 choices=(('starter', 'entrée'),
                                          ('meal', 'plat'),
                                          ('dessert', 'dessert')),
                                 verbose_name='type de recette',
                                 )
    parts = models.IntegerField(verbose_name='nombre de parts')
    picture = ImageField(upload_to='recipe', verbose_name='image', blank=True)
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
                                            verbose_name='recettes de base',
                                            through=ParentRecipe,
                                            through_fields=('child', 'parent'),
                                            symmetrical=False,
                                            related_name='children_recipes')
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient,
                                         verbose_name='ingrédients')
    ustensils = models.ManyToManyField(Ustensil, blank=True,
                                       verbose_name='ustensiles')
    diets = models.ManyToManyField(Diet, verbose_name='régimes')

    def __str__(self):
        return self.name

    def picture_str(self):
        thumb = get_thumbnail(self.picture, '100x100', crop='center')
        if thumb:
            return '<img src="{}" alt="" />'.format(thumb.url)
        else:
            return ''
    picture_str.short_description = 'Image'
    picture_str.allow_tags = True

    def get_diets(self):
        """ return the list of diets for this recipe.
        """
        diets = [[d for d in i.diets.all()]
                 for i in self.ingredients.all()]
        total_diets = set()
        for diet in diets:
            if len(total_diets) == 0:
                total_diets = set(diet)
            total_diets = total_diets.intersection(diet)
        for cur_diet in self.diets.all():
            if cur_diet not in total_diets:
                self.diets.remove(cur_diet)
        self.diets.add(*total_diets)

    def diets_str(self):
        diets = [d.name for d in self.diets.all()]
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

    def get_absolute_url(self):
        return resolve_url('recipe_detail', pk=self.pk)

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
                if self.diet in r.diets.all()]

    def __str__(self):
        return '{meal} — {count} × {diet}'.format(meal=self.meal,
                                                  count=self.count,
                                                  diet=self.diet_name())

    class Meta:
        verbose_name = 'participant à un repas'
        verbose_name_plural = 'participants à un repas'


class Meal(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')
    date = models.DateTimeField(verbose_name='Date et heure')
    recipes = models.ManyToManyField(Recipe, verbose_name='recettes')
    session = models.ForeignKey('Session', blank=True, null=True)

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
            # first, we get the total number of parts we have to make (we only
            # count diet-compatible participants).
            # then, we calculate the total number of this recipe that will be
            # needed.
            parts_count = self.recipe_diet_participants()[recipe]
            recipe_count = ceil(parts_count / recipe.parts)
            for recipe_ingredient in recipe.recipeingredient_set.all():
                if recipe_ingredient.quantity * recipe_count > 0:
                    if recipe_ingredient.ingredient not in ingredients:
                        ingredients[recipe_ingredient.ingredient] = 0
                    ingredients[recipe_ingredient.ingredient] += \
                        recipe_ingredient.quantity * recipe_count

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
        price = sum([i['price'] for i in self.ingredients_list()])
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
            diets = recipe.diets.all()
            for diet in diets:
                participants[recipe] += sum([p.count for p in
                                             self.mealparticipant_set
                                             .filter(diet__name=diet)])
        return participants

    @method_cache()
    def warnings(self):
        """returns a list of warnings concerning this meal (does a recipe not
        have any compatible participant? Cannot a participant eat something?)
        """
        warnings = OrderedDict()
        for recipe, part in self.recipe_diet_participants().items():
            if part == 0:
                warnings[recipe] = ('Personne ne peut manger {}'.format(recipe))
        for part in self.participants():
            if not part.can_eat():
                warnings[part] = ('{} {}{} ne peu{}t rien manger'
                                  .format(part.count,
                                          part.diet,
                                          pluralize(part.count),
                                          pluralize(part.count, 'ven')))

        return warnings

    def admin_warnings(self):
        warnings = self.warnings().values()
        if len(warnings):
            return '\n'.join(['<p class="text-danger"><span class="glyphicon '
                              'glyphicon-exclamation-sign"></span> {}</p>\n'
                              .format(s) for s in warnings])
        else:
            return '<p class="text-success"><span class="glyphicon '\
                'glyphicon-ok-sign"></span> Tout va bien ♥</p>'
    admin_warnings.short_description = 'Avertissements'
    admin_warnings.allow_tags = True

    @method_cache()
    def status(self):
        """returns whether this meal is complete (has something for each
        participant) or not.
        """
        return len(self.warnings()) == 0
    status.short_description = 'Statut'

    def admin_roadmap(self):
        return '<a href="{url}" title="Générer la feuille de route" '\
               'target="_blank"><span class=" glyphicon glyphicon-list">'\
               '</span></a>'.format(
                   url=resolve_url('roadmap_meal',
                                   meal_id=self.id))
    admin_roadmap.short_description = 'Feuille de route'
    admin_roadmap.allow_tags = True

    class Meta:
        verbose_name = 'repas'
        verbose_name_plural = 'repas'


class Session(models.Model):

    name = models.CharField(max_length=100, verbose_name='nom')

    def calendar(self):
        """generates calendars representing all meals in the session, as a list
        of Calendar.monthdatescalendar() lists.
        In those lists, the second values of tuples are the corresponding Meal
        objects.
        """
        cur_month = None

        meals = self.meal_set.order_by('date')
        meals_dates = {}
        meals_count = 0
        for meal in meals:
            cur_month = meal.date if cur_month is None else cur_month
            meals_count += 1
            if meal.date not in meals_dates:
                if meal.date.date() not in meals_dates:
                    meals_dates[meal.date.date()] = []
            meals_dates[meal.date.date()].append(meal)

        if not cur_month:
            cur_month = datetime.now()

        months = []

        cal = Calendar()
        month = cal.monthdatescalendar(cur_month.year, cur_month.month)
        remaining_meals = meals_count
        while remaining_meals > 0:
            month = cal.monthdatescalendar(cur_month.year, cur_month.month)
            for i, month_week in enumerate(month):
                for j, day in enumerate(month_week):
                    meal_dates = meals_dates[day] if day in meals_dates and \
                        day.month == cur_month.month else []
                    remaining_meals -= len(meal_dates)
                    month[i][j] = {'date': month[i][j], 'meals': meal_dates}
            months.append({'month': cur_month, 'dates': month})
            cur_month = cur_month + relativedelta(months=1)
        return months

    @method_cache()
    def ingredients_list(self):
        """returns a list of ingredients needed for all recipes in all meals of
        this session. The ingredients are returned as dicts containing the
        Ingredient itself, the quantity needed, and the total price of that
        ingredient.
        """
        ingredients = OrderedDict()
        for meal in self.meal_set.order_by('date'):
            for ingredient in meal.ingredients_list():
                if ingredient['ingredient'] in ingredients:
                    ingredients[ingredient['ingredient']]['quantity'] += \
                        ingredient['quantity']
                    ingredients[ingredient['ingredient']]['price'] += \
                        ingredient['price']
                else:
                    ingredients[ingredient['ingredient']] = ingredient
                    ingredients[ingredient['ingredient']]['date'] = \
                        meal.date
        ingredients_list = [i for i in ingredients.values()]
        return ingredients_list

    @method_cache()
    def total_price(self):
        """returns the sum of the individual price of each ingredient in each
        recipe of each meal of this session.
        """
        price = sum([i['price'] for i in self.ingredients_list()])
        return price

    def meals(self):
        """returns the Meal list, ordered by date.
        """
        return self.meal_set.order_by('date')

    def admin_roadmap(self):
        return '<a href="{url}" title="Générer la feuille de route" '\
               'target="_blank"><span class=" glyphicon glyphicon-list">'\
               '</span></a>'.format(url=resolve_url('roadmap_session',
                                    session_id=self.id))
    admin_roadmap.short_description = 'Feuille de route'
    admin_roadmap.allow_tags = True

    @method_cache()
    def warnings(self):
        """returns a list of warnings concerning this session
        """
        warnings_list = [m.warnings() for m in self.meal_set.all()]
        warnings = OrderedDict()
        for warning in warnings_list:
            warnings.update(warning)
        return warnings

    def admin_warnings(self):
        warnings = self.warnings().values()
        if len(warnings):
            return '\n'.join(['<p class="text-danger"><span class="glyphicon '
                              'glyphicon-exclamation-sign"></span> {}</p>\n'
                              .format(s) for s in warnings])
        else:
            return '<p class="text-success"><span class="glyphicon '\
                'glyphicon-ok-sign"></span> Tout va bien ♥</p>'
    admin_warnings.short_description = 'Avertissements'
    admin_warnings.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'session'
