# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-03 15:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_auto_20170203_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='first_visit',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 3, 15, 29, 9, 690000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='page',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 3, 15, 29, 9, 690000, tzinfo=utc)),
        ),
    ]
