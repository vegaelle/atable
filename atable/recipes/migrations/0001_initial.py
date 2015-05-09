# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('providers', models.TextField()),
                ('diets', models.ManyToManyField(to='recipes.Diet')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MealParticipant',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('diet', models.ForeignKey(to='recipes.Diet')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('meal_type', models.CharField(max_length=10, choices=[('meal', 'Meal'), ('dessert', 'Dessert')])),
                ('parts', models.IntegerField()),
                ('picture', models.ImageField(upload_to='recipe')),
                ('preparation_time', models.DurationField()),
                ('cooking_time', models.DurationField()),
                ('description', models.TextField()),
                ('licence', models.TextField()),
                ('author', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SessionMeal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal', models.ForeignKey(to='recipes.Meal')),
                ('session', models.ForeignKey(to='recipes.Session')),
            ],
        ),
        migrations.CreateModel(
            name='Ustensil',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='meals',
            field=models.ManyToManyField(to='recipes.Meal', through='recipes.SessionMeal'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient', through='recipes.RecipeIngredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(related_name='parent_recipes_rel_+', to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ustensils',
            field=models.ManyToManyField(to='recipes.Ustensil'),
        ),
        migrations.AddField(
            model_name='meal',
            name='participants',
            field=models.ManyToManyField(to='recipes.MealParticipant'),
        ),
        migrations.AddField(
            model_name='meal',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe'),
        ),
    ]
