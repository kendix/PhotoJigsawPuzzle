# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-04 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umdPuzzle', '0002_auto_20161204_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(help_text='name of the location/puzzle', max_length=100, unique=True),
        ),
    ]
