# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 14:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date_expired',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 14, 58, 26, 764093)),
        ),
        migrations.AlterModelTable(
            name='session',
            table='session',
        ),
    ]
