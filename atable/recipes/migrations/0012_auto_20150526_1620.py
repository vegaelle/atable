# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20150521_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='diets',
            field=models.ManyToManyField(verbose_name='régimes', to='recipes.Diet'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='diets',
            field=models.ManyToManyField(verbose_name='régimes', to='recipes.Diet'),
        ),
    ]
