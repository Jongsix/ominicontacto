# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-06 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0109_queue_detectar_contestadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitioexterno',
            name='oculto',
            field=models.BooleanField(default=False),
        ),
    ]
