# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wxuser',
            name='login_flag',
        ),
        migrations.AlterField(
            model_name='wxuser',
            name='icon_url',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='wxuser',
            name='province',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='wxuser',
            name='wx_icon',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='wxuser',
            name='wx_nickname',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
