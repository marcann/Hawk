# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 16:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_calendar', '0003_auto_20160831_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 31, 12, 59, 38, 255145), verbose_name='Date and time'),
        ),
    ]