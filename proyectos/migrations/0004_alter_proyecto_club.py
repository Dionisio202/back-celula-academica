# Generated by Django 5.0.6 on 2024-06-21 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_alter_proyecto_club'),
        ('proyectos', '0003_remove_proyecto_clubs_proyecto_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_asociados', to='clubs.club'),
        ),
    ]
