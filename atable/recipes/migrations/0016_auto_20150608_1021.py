# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20150604_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentRecipe',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='parent_recipes',
        ),
        migrations.AddField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(to='recipes.Recipe', blank=True, verbose_name='recettes de base', through='recipes.ParentRecipe'),
        ),
        migrations.AddField(
            model_name='parentrecipe',
            name='child',
            field=models.ForeignKey(to='recipes.Recipe', verbose_name='recette enfant', related_name='child_recipes'),
        ),
        migrations.AddField(
            model_name='parentrecipe',
            name='parent',
            field=models.ForeignKey(to='recipes.Recipe', verbose_name='recette parente'),
        ),
    ]
