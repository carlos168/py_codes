# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-05 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='st_power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miner', models.CharField(max_length=32)),
                ('user', models.CharField(max_length=32)),
            ],
        ),
    ]
