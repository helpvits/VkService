# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-16 06:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parcer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupslist',
            name='author',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]