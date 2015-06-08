# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20150608_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(upload_to='recipe', blank=True, verbose_name='image'),
        ),
    ]
