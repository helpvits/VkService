# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-16 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parcer', '0004_auto_20170616_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='deltaparse',
            name='incoming',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deltaparse',
            name='leavers',
            field=models.TextField(blank=True, null=True),
        ),
    ]
