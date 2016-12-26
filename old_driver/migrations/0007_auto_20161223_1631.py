# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old_driver', '0006_auto_20161217_0836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('album_id', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to='old_driver.WxUser', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(to='old_driver.Album', null=True),
        ),
    ]
