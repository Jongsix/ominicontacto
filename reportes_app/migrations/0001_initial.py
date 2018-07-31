# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-07-31 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadAgenteLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True)),
                ('agente_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('event', models.CharField(blank=True, max_length=32, null=True)),
                ('pausa_id', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LlamadaLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True)),
                ('callid', models.CharField(blank=True, max_length=32, null=True)),
                ('campana_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('tipo_campana', models.IntegerField(blank=True, null=True)),
                ('tipo_llamada', models.IntegerField(blank=True, null=True)),
                ('agente_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('event', models.CharField(blank=True, max_length=32, null=True)),
                ('numero_marcado', models.CharField(blank=True, max_length=128, null=True)),
                ('contacto_id', models.IntegerField(blank=True, null=True)),
                ('bridge_wait_time', models.IntegerField(blank=True, null=True)),
                ('duracion_llamada', models.IntegerField(blank=True, null=True)),
                ('archivo_grabacion', models.CharField(blank=True, max_length=50, null=True)),
                ('agente_extra_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('campana_destino_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('numero_destino', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
    ]
