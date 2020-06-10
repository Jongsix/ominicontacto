# Generated by Django 2.2.7 on 2020-06-01 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0054_crear_roles_predefinidos'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditoriaCalificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.IntegerField(choices=[(0, 'Aprobada'), (1, 'Rechazada'), (2, 'Observada')])),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('calificacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.CalificacionCliente')),
            ],
        ),
    ]