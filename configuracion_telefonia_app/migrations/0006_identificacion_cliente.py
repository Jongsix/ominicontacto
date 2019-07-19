# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-06-06 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0020_remove_campana_formulario'),
        ('configuracion_telefonia_app', '0005_rutasaliente_orden'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdentificadorCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('tipo_interaccion', models.PositiveIntegerField(
                    choices=[(1, 'Sin interacci\xf3n externa'),
                             (2, 'Interacci\xf3n externa tipo 1'),
                             (3, 'Interacci\xf3n externa tipo 2')],
                    default=1,
                    help_text='Tipo de interacci\xf3n',
                    verbose_name='Tipo de interacci\xf3n')),
                ('url', models.CharField(blank=True, max_length=128, null=True,
                                         verbose_name='Url servicio identificaci\xf3n')),
                ('longitud_id_esperado', models.PositiveIntegerField(
                    blank=True,
                    null=True,
                    validators=[django.core.validators.MaxValueValidator(30)],
                    verbose_name='Longitud de id esperado')),
                ('timeout', models.PositiveIntegerField(
                    default=5,
                    validators=[django.core.validators.MaxValueValidator(60)],
                    verbose_name='Timeout')),
                ('intentos', models.PositiveIntegerField(
                    default=1,
                    validators=[django.core.validators.MinValueValidator(1),
                                django.core.validators.MaxValueValidator(20)],
                    verbose_name='Intentos')),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                            related_name='identificadores_cliente',
                                            to='ominicontacto_app.ArchivoDeAudio')),
            ],
        ),
        migrations.AlterField(
            model_name='destinoentrante',
            name='tipo',
            field=models.PositiveIntegerField(
                choices=[(1, 'Campa\xf1a entrante'),
                         (2, 'Validaci\xf3n de fecha/hora'),
                         (3, 'IVR'),
                         (5, 'HangUp'),
                         (9, 'Identificador cliente')]),
        ),
    ]