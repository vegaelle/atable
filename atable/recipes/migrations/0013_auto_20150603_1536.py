# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from ..models import Recipe


def refresh_diets(apps, schema_editor):
    for rec in Recipe.objects.all():
        rec.get_diets()


def unrefresh_diets(apps, schema_editor):
    """running this migration backwards has no effect.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20150526_1620'),
    ]

    operations = [
        migrations.RunPython(refresh_diets, unrefresh_diets),
    ]
