# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxuser',
            name='group',
            field=models.ForeignKey(related_name='group', default=None, to='old_driver.Group'),
        ),
    ]
