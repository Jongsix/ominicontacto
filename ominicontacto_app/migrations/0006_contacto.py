# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 19:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0005_basedatoscontacto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cliente', models.IntegerField()),
                ('nombre', models.CharField(max_length=128)),
                ('apellido', models.CharField(max_length=128)),
                ('telefono', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('datos', models.TextField()),
                ('bd_contacto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactos', to='ominicontacto_app.BaseDatosContacto')),
            ],
        ),
    ]