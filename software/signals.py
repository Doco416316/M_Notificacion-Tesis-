# software/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.models import Notificacion
from software.models import Software, Hardware

@receiver(post_save, sender=Software)
@receiver(post_save, sender=Hardware)
def crear_notificacion_cambio(sender, instance, created, **kwargs):
    if created:
        mensaje = f'Se ha agregado {sender.__name__.lower()} "{instance.nombre}".'
        prioridad = 'alta'  # Aquí puedes implementar la lógica para determinar la prioridad
    else:
        mensaje = f'Se ha actualizado {sender.__name__.lower()} "{instance.nombre}".'
        prioridad = 'media'  # Otra lógica de prioridad
    Notificacion.objects.create(tipo=sender.__name__.lower(), mensaje=mensaje, prioridad=prioridad)

@receiver(post_delete, sender=Software)
@receiver(post_delete, sender=Hardware)
def crear_notificacion_eliminacion(sender, instance, **kwargs):
    mensaje = f'Se ha eliminado {sender.__name__.lower()} "{instance.nombre}".'
    prioridad = 'baja'  # Prioridad para eliminación
    Notificacion.objects.create(tipo=sender.__name__.lower(), mensaje=mensaje, prioridad=prioridad)
