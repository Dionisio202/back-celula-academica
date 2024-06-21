#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt


# Apply any outstanding database migrations
python manage.py migrate


# Crea un superusuario (sustituye 'superuser' por los valores que desees)
echo "from users.models import CustomUser
from django.contrib.auth.models import Group
group = Group.objects.create(name='Administradores')
superuser = CustomUser.objects.create_superuser(
    email='eortiz5364@uta.edu.ec',
    cedula='1850085364',
    telefono='0983860122',
    carrera='Software',
    semestre=6,
    categoria=group,
    password='123456',
    nombre='Edison',
    apellido='Ortiz'
)" | python manage.py shell

# Convert static asset files
python manage.py collectstatic --no-input