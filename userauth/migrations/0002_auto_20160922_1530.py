# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-22 19:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name'], 'verbose_name': 'User Group', 'verbose_name_plural': 'User Groups'},
        ),
    ]