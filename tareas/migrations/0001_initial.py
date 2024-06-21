# Generated by Django 5.0.4 on 2024-05-07 03:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyectos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_limite', models.DateField()),
                ('estado', models.CharField(choices=[('sin_asignar', 'Sin asignar'), ('en_proceso', 'En proceso'), ('en_espera', 'En espera'), ('terminado', 'Terminado'), ('otro', 'Otro')], default='sin_asignar', max_length=20)),
                ('fotografias', models.ImageField(blank=True, null=True, upload_to='tareas')),
                ('miembros_responsables', models.ManyToManyField(related_name='tareas_responsables', to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='proyectos.proyecto')),
            ],
        ),
    ]