from django.db import models
from users.models import CustomUser
from proyectos.models import Proyecto

class Tarea(models.Model):
    ESTADOS_CHOICES = [
        ('sin_asignar', 'Sin asignar'),
        ('en_proceso', 'En proceso'),
        ('en_espera', 'En espera'),
        ('terminado', 'Terminado'),
        ('otro', 'Otro'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='sin_asignar')
    fotografias = models.ImageField(upload_to='tareas', blank=True, null=True)
    miembros_responsables = models.ManyToManyField(CustomUser, related_name='tareas_responsables')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')

    def __str__(self):
        return self.nombre
