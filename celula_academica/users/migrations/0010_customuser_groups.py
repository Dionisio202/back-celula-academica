# Generated by Django 5.0.4 on 2024-05-07 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0009_rename_usuariosregistrados_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_groups', to='auth.group'),
        ),
    ]
