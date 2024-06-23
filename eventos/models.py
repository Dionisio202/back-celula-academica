from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Ponente(models.Model):
    cedula = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener exactamente 10 dígitos y solo números.')]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el nombre.')]
    )
    apellido = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el apellido.')]
    )
    correo = models.EmailField()
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'El teléfono debe tener exactamente 10 dígitos y solo números.')]
    )
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
    valor_inscripcion = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.0, "El valor de la inscripción no puede ser negativo.")]
    )

    def __str__(self):
        return self.nombre
    
class Charla(Evento):
    ponentes = models.ManyToManyField(Ponente)
    imagen = models.ImageField(upload_to='charlas', null=True, blank=True)

class InscripcionConcurso(models.Model):
    cedula = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener exactamente 10 dígitos y solo números.')]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el nombre.')]
    )
    apellido = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el apellido.')]
    )
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'El teléfono debe tener exactamente 10 dígitos y solo números.')]
    )
    correo = models.EmailField()
    carrera = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para la carrera.')]
    )
    semestre = models.PositiveIntegerField(
        validators=[MinValueValidator(0, "El semestre debe ser un número entre 0 y 10"), MaxValueValidator(10, "El semestre debe ser un número entre 0 y 10")]
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='inscripciones')
    nombre_grupo = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.concurso.nombre}'

    def clean(self):
        super().clean()
        if self.concurso.max_integrantes is not None:
            if not self.nombre_grupo or any(char.isdigit() for char in self.nombre_grupo):
                raise ValidationError('El nombre de grupo no puede contener números ni estar en blanco ')
            else:
                 integrantes_actuales = self.concurso.inscripciones.filter(nombre_grupo=self.nombre_grupo).count()
                 if integrantes_actuales >= self.concurso.max_integrantes:
                    raise ValidationError('Se ha alcanzado el número máximo de integrantes para ese nombre de grupo.')
        elif self.nombre_grupo:
            raise ValidationError('No puede ingresar un nombre de grupo si el concurso no permite grupos.')
      
    def nombre_grupo_visible(self):
        return not self.concurso.competencia_individual