# Generated by Django 5.0.4 on 2024-06-01 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('competencia_individual', models.BooleanField()),
                ('max_integrantes', models.PositiveIntegerField(blank=True, null=True)),
                ('valor_inscripcion', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='ponente',
            name='hora_fin',
        ),
        migrations.RemoveField(
            model_name='ponente',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='ponente',
            name='tema_charla',
        ),
        migrations.CreateModel(
            name='Charla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('tema_charla', models.CharField(max_length=200)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('ponentes', models.ManyToManyField(to='eventos.ponente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Evento',
        ),
    ]
