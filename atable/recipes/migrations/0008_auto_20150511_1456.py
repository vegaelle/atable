# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20150511_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diet',
            options={'verbose_name': 'régime'},
        ),
        migrations.RemoveField(
            model_name='meal',
            name='participants',
        ),
        migrations.AddField(
            model_name='mealparticipant',
            name='meal',
            field=models.ForeignKey(verbose_name='repas', to='recipes.Meal', default=1),
            preserve_default=False,
        ),
    ]
