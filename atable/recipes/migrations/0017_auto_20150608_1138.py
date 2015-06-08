# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20150608_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentrecipe',
            name='child',
            field=models.ForeignKey(to='recipes.Recipe', related_name='parentrecipe_set', verbose_name='recette enfant'),
        ),
        migrations.AlterField(
            model_name='parentrecipe',
            name='parent',
            field=models.ForeignKey(to='recipes.Recipe', related_name='childrecipe_set', verbose_name='recette parente'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(to='recipes.Recipe', blank=True, through='recipes.ParentRecipe', related_name='children_recipes', verbose_name='recettes de base'),
        ),
    ]
