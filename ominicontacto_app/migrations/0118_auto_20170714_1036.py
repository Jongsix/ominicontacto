# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-14 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0117_supervisorprofile_is_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacioncliente',
            name='contacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.Contacto'),
        ),
    ]
