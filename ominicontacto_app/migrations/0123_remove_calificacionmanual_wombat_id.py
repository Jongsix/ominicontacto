# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-03 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0122_auto_20170802_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calificacionmanual',
            name='wombat_id',
        ),
    ]