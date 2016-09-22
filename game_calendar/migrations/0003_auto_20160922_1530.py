# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-22 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_calendar', '0002_auto_20160922_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='comments',
        ),
        migrations.AlterField(
            model_name='event',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.Group'),
        ),
    ]