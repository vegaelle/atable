# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20150510_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'ingrédient'},
        ),
        migrations.AlterModelOptions(
            name='meal',
            options={'verbose_name_plural': 'repas', 'verbose_name': 'repas'},
        ),
        migrations.AlterModelOptions(
            name='mealparticipant',
            options={'verbose_name_plural': 'participants à un repas', 'verbose_name': 'participant à un repas'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'recette'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name_plural': 'ingrédients de recette', 'verbose_name': 'ingrédient de recette'},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name': 'session'},
        ),
        migrations.AlterModelOptions(
            name='sessionmeal',
            options={'verbose_name_plural': 'repas de session', 'verbose_name': 'repas de session'},
        ),
        migrations.AlterModelOptions(
            name='ustensil',
            options={'verbose_name': 'ustensile'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='diets',
            field=models.ManyToManyField(to='recipes.Diet', blank=True, verbose_name='régimes'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='price',
            field=models.FloatField(verbose_name='prix'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='providers',
            field=models.TextField(blank=True, verbose_name='fournisseurs'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(max_length=100, verbose_name='unité'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='begin',
            field=models.TimeField(help_text='Entrez l’heure de début, au format HH:MM:SS', verbose_name='heure de début'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='end',
            field=models.TimeField(help_text='Entrez l’heure de fin, au format HH:MM:SS', verbose_name='heure de fin'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='participants',
            field=models.ManyToManyField(related_name='meal', blank=True, to='recipes.MealParticipant', verbose_name='participants'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe', verbose_name='recettes'),
        ),
        migrations.AlterField(
            model_name='mealparticipant',
            name='count',
            field=models.IntegerField(verbose_name='nombre de personnes'),
        ),
        migrations.AlterField(
            model_name='mealparticipant',
            name='diet',
            field=models.ForeignKey(to='recipes.Diet', verbose_name='régime'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.CharField(max_length=100, default='La Grande Ourse', verbose_name='auteur'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(null=True, help_text='Entrez le temps de cuisson requis, au format HH:MM:SS. Laissez vide si non nécessaire.', blank=True, verbose_name='temps de cuisson'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(verbose_name='descriptif de la recette'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient', through='recipes.RecipeIngredient', verbose_name='ingrédients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='licence',
            field=models.TextField(default='\n<h2> CC0 1.0 universel (CC0 1.0)</h2>\n<em>Transfert dans le Domaine Public</em>\n\n<h3>Cette licence est acceptable pour des œuvres culturelles libres.</h3>\n\n<p>La personne qui a associé une œuvre à cet acte a dédié l’œuvre au domaine\npublic en renonçant dans le monde entier à ses droits sur l’œuvre selon les\nlois sur le droit d’auteur, droit voisin et connexes, dans la mesure permise\npar la loi.</p>\n\n<p>Vous pouvez copier, modifier, distribuer et représenter l’œuvre, même à des\nfins commerciales, sans avoir besoin de demander l’autorisation. Voir d’autres\ninformations ci-dessous.</p>\n\n<h3>Autres informations</h3>\n\n<ul>\n<li>Les brevets et droits de marque commerciale qui peuvent être détenus par\nautrui ne sont en aucune façon affectés par CC0, de même pour les droits que\npourraient détenir d’autres personnes sur l’œuvre ou sur la façon dont elle est\nutilisée, comme le droit à l’image ou à la vie privée.</li>\n<li>À moins d’une mention expresse contraire, la personne qui a identifié une\nœuvre à cette notice ne concède aucune garantie sur l’œuvre et décline toute\nresponsabilité de toute utilisation de l’œuvre, dans la mesure permise par la\nloi.</li>\n<li>Quand vous utilisez ou citez l’œuvre, vous ne devez pas sous-entendre le\nsoutien de l’auteur ou de la personne qui affirme.</li>\n</ul>', blank=True, verbose_name='licence'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='meal_type',
            field=models.CharField(max_length=10, choices=[('meal', 'plat'), ('dessert', 'dessert')], verbose_name='type de recette'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(related_name='parent_recipes_rel_+', blank=True, to='recipes.Recipe', verbose_name='recettes parentes'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='parts',
            field=models.IntegerField(verbose_name='nombre de parts'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='picture',
            field=models.ImageField(upload_to='recipe', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.DurationField(null=True, help_text='Entrez le temps de préparation requis, au format HH:MM:SS. Laissez vide si non nécessaire.', blank=True, verbose_name='temps de préparation'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ustensils',
            field=models.ManyToManyField(to='recipes.Ustensil', blank=True, verbose_name='ustensiles'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(to='recipes.Ingredient', verbose_name='ingrédient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.IntegerField(verbose_name='quantité'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(to='recipes.Recipe', verbose_name='recette'),
        ),
        migrations.AlterField(
            model_name='session',
            name='meals',
            field=models.ManyToManyField(to='recipes.Meal', through='recipes.SessionMeal', verbose_name='repas'),
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='sessionmeal',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='sessionmeal',
            name='meal',
            field=models.ForeignKey(to='recipes.Meal', verbose_name='repas'),
        ),
        migrations.AlterField(
            model_name='sessionmeal',
            name='session',
            field=models.ForeignKey(to='recipes.Session', verbose_name='session'),
        ),
        migrations.AlterField(
            model_name='ustensil',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nom'),
        ),
    ]
