# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20150509_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(blank=True, related_name='parent_recipes_rel_+', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ustensils',
            field=models.ManyToManyField(blank=True, to='recipes.Ustensil'),
        ),
    ]
