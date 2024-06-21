from django.db import models
from users.models import CustomUser
from clubs.models import Club

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proyectos_creados')
    miembros = models.ManyToManyField(CustomUser, related_name='proyectos')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='proyectos_asociados', null=False, blank=False)

    def __str__(self):
        return self.nombre
