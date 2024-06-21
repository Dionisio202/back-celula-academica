from django.db import models
from users.models import CustomUser

User = CustomUser()

class Club(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs_responsable')
    miembros = models.ManyToManyField(User, related_name='clubs_miembro', blank=True)

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='proyectos_del_club')

    def __str__(self):
        return self.nombre
