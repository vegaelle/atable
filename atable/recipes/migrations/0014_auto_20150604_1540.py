# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.db import models, migrations


def store_date_in_meal(apps, schema_editor):
    """We will take every sessionMeal object, and make a DateTime object from
    its date and its meal's time. Then we’ll store that DateTime in the Meal
    object.
    """
    SessionMeal = apps.get_model('recipes', 'SessionMeal')
    for session_meal in SessionMeal.objects.all():
        date = datetime.combine(session_meal.date,
                                session_meal.meal.begin)
        session_meal.meal.date = date
        session_meal.meal.save()


def unstore_date_in_meal(apps, schema_editor):
    """ we will take every Meal object, extract its DateTime, and store the time
    in the meal, and the time part in the SessionMeal object.
    """
    SessionMeal = apps.get_model('recipes', 'SessionMeal')
    for session_meal in SessionMeal.objects.all():
        date = session_meal.meal.date
        session_meal.meal.begin = date.time()
        session_meal.date = date.date()
        session_meal.meal.end = (date + timedelta(hours=1)).time()
        session_meal.meal.save()
        session_meal.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20150603_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='diets',
        ),
        migrations.AddField(
            model_name='meal',
            name='date',
            field=models.DateTimeField(verbose_name='Date et heure',
                                       default=datetime(1970, 1, 1, 0, 0)),
            preserve_default=False,
        ),
        migrations.RunPython(store_date_in_meal, unstore_date_in_meal),
    ]
