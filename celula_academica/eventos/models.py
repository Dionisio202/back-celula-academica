from django.db import models
import datetime

class Ponente(models.Model):
    cedula = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    biografia = models.TextField()
    hora_inicio = models.TimeField(null=True)
    hora_fin = models.TimeField(null=True)
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        abstract = True

class Concurso(Evento):
    competencia_individual = models.BooleanField()
    max_integrantes = models.PositiveIntegerField(null=True, blank=True)
    valor_inscripcion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class Charla(Evento):
    ponentes = models.ManyToManyField(Ponente)
    imagen = models.ImageField(upload_to='charlas', null=True, blank=True)

class InscripcionConcurso(models.Model):
    cedula = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    carrera = models.CharField(max_length=100)
    semestre = models.PositiveIntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='inscripciones')

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.concurso.nombre}'
