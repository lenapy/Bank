# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-27 14:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_auto_20170927_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='date_expired',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 4, 14, 27, 19, 75154)),
        ),
    ]
