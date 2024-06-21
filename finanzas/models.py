# models.py
from django.db import models
from eventos.models import Concurso, InscripcionConcurso

class PagoInscripcion(models.Model):
    inscripcion = models.ForeignKey(InscripcionConcurso, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pago de {self.inscripcion.nombre} {self.inscripcion.apellido} para {self.inscripcion.concurso.nombre}'

class IngresoEconomico(models.Model):
    fecha_ingreso = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_ingreso = models.CharField(max_length=50, choices=[
        ('donacion', 'Donación'),
        ('concurso', 'Concurso'),
        # otros tipos de ingresos
    ])
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Ingreso de {self.monto} el {self.fecha_ingreso}'

class EgresoEconomico(models.Model):
    fecha_egreso = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    tipo_egreso = models.CharField(max_length=50, choices=[
        ('pagos', 'Pagos'),
        ('concurso', 'Concurso'),
        # otros tipos de egresos
    ])
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Egreso de {self.monto} el {self.fecha_egreso}'
