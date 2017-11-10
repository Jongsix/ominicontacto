# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-10-25 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0130_agenteencontacto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenteencontacto',
            name='estado',
            field=models.PositiveIntegerField(choices=[(0, 'INICIAL'), (1, 'ENTREGADO'),
                                                       (2, 'ATENDIENDO'), (3, 'FINALIZADO')]),
        ),
    ]