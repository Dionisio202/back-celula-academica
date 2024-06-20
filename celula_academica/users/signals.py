# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .views import send_reset_password_email

@receiver(post_save, sender=CustomUser)
def enviar_correo_bienvenida(sender, instance, created, **kwargs):
    if created:
        send_reset_password_email(instance)
