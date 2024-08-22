# hardware/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.models import Notificacion
from hardware.models import Hardware

@receiver(post_save, sender=Hardware)
def crear_notificacion_cambio_hardware(sender, instance, created, **kwargs):
    if created:
        mensaje = f'Se ha agregado hardware "{instance.nombre}".'
        prioridad = 'alta'  # Lógica de prioridad para creación
    else:
        mensaje = f'Se ha actualizado hardware "{instance.nombre}".'
        prioridad = 'media'  # Lógica de prioridad para actualización
    Notificacion.objects.create(tipo='hardware', mensaje=mensaje, prioridad=prioridad)

@receiver(post_delete, sender=Hardware)
def crear_notificacion_eliminacion_hardware(sender, instance, **kwargs):
    mensaje = f'Se ha eliminado hardware "{inst
