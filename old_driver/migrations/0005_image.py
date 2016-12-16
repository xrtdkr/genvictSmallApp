# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0004_auto_20161215_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=10, blank=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('url', models.CharField(max_length=100, blank=True)),
                ('message', models.CharField(max_length=50, blank=True)),
                ('longitude', models.CharField(max_length=30, blank=True)),
                ('latitude', models.CharField(max_length=30, blank=True)),
                ('datetime', models.CharField(max_length=30, blank=True)),
                ('user', models.ForeignKey(to='old_driver.WxUser')),
            ],
        ),
    ]
