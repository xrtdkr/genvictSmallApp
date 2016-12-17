# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0005_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
