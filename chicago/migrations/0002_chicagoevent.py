# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-25 19:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councilmatic_core', '0027_merge'),
        ('chicago', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChicagoEvent',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('councilmatic_core.event',),
        ),
    ]
