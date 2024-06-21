# Generated by Django 5.0.4 on 2024-05-07 02:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_creados', to=settings.AUTH_USER_MODEL)),
                ('miembros', models.ManyToManyField(related_name='proyectos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]