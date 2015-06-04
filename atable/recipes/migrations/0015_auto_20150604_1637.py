# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_session(apps, schema_editor):
    """We will take every SessionMeal object, and store the Session in the Meal
    directly.
    """
    SessionMeal = apps.get_model('recipes', 'SessionMeal')
    for session_meal in SessionMeal.objects.all():
        session_meal.meal.session = session_meal.session


def set_session_meal(apps, schema_editor):
    """We will take every Meal, and create a SessionMeal object instead.
    """
    SessionMeal = apps.get_model('recipes', 'SessionMeal')
    Meal = apps.get_model('recipes', 'Meal')
    for meal in Meal.objects.all():
        if meal.session:
            sm = SessionMeal(meal=meal, session=meal.session)
            sm.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20150604_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='begin',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='end',
        ),
        migrations.RemoveField(
            model_name='sessionmeal',
            name='date',
        ),
        migrations.AddField(
            model_name='meal',
            name='session',
            field=models.ForeignKey(related_name='session_meals', null=True,
                                    to='recipes.Session', blank=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='meals',
            field=models.ManyToManyField(verbose_name='repas',
                                         to='recipes.Meal',
                                         through='recipes.SessionMeal',
                                         related_name='sessions'),
        ),
        migrations.RunPython(set_session, set_session_meal),
        migrations.RemoveField(
            model_name='sessionmeal',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='sessionmeal',
            name='session',
        ),
        migrations.RemoveField(
            model_name='session',
            name='meals',
        ),
        migrations.DeleteModel(
            name='SessionMeal',
        ),
        migrations.AlterField(
            model_name='meal',
            name='session',
            field=models.ForeignKey(to='recipes.Session', blank=True,
                                    null=True),
        ),
    ]
