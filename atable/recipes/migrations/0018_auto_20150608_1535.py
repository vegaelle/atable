# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20150608_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parentrecipe',
            options={'verbose_name_plural': 'recettes parentes', 'verbose_name': 'recette parente'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='meal_type',
            field=models.CharField(max_length=10, choices=[('starter', 'entrée'), ('meal', 'plat'), ('dessert', 'dessert')], verbose_name='type de recette'),
        ),
    ]
