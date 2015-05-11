# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20150511_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealparticipant',
            name='diet',
            field=models.ForeignKey(to='recipes.Diet', help_text='Laissez vide si pas de régime spécial', blank=True, null=True, verbose_name='régime'),
        ),
    ]
