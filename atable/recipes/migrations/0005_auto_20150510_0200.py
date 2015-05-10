# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20150510_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='participants',
            field=models.ManyToManyField(blank=True, to='recipes.MealParticipant'),
        ),
    ]
