# Generated by Django 5.0.6 on 2024-06-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0009_alter_concurso_valor_inscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcionconcurso',
            name='nombre_grupo',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
