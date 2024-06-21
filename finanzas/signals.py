# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PagoInscripcion, IngresoEconomico

@receiver(post_save, sender=PagoInscripcion)
def registrar_ingreso_economico(sender, instance, created, **kwargs):
    if created:
        IngresoEconomico.objects.create(
            fecha_ingreso=instance.fecha_pago,
            monto=instance.monto,
            tipo_ingreso='concurso',
            concurso=instance.inscripcion.concurso
        )
