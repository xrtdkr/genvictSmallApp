# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0003_auto_20161215_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_id',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='wxuser',
            name='group',
            field=models.ForeignKey(to='old_driver.Group'),
        ),
    ]
