# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20150510_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='providers',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='licence',
            field=models.TextField(blank=True),
        ),
    ]
