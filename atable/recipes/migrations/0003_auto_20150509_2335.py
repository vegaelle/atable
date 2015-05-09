# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20150509_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(related_name='parent_recipes_rel_+', to='recipes.Recipe', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ustensils',
            field=models.ManyToManyField(to='recipes.Ustensil', null=True, blank=True),
        ),
    ]
