# Importa las señales post_save y post_delete, y el receptor de señales
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Importa el modelo Notificacion desde el módulo de notificaciones
from notifications.models import Notificacion
# Importa los modelos Software y Hardware desde el módulo actual
from software.models import Software, Hardware

# Define un receptor de señal para cuando se guarda un objeto Software o Hardware
@receiver(post_save, sender=Software)
@receiver(post_save, sender=Hardware)
def crear_notificacion_cambio(sender, instance, created, **kwargs):
    # Verifica si el objeto ha sido creado
    if created:
        # Crea un mensaje para la notificación de creación
        mensaje = f'Se ha agregado {sender.__name__.lower()} "{instance.nombre}".'
        # Define la prioridad para la creación
        prioridad = 'alta'
    else:
        # Crea un mensaje para la notificación de actualización
        mensaje = f'Se ha actualizado {sender.__name__.lower()} "{instance.nombre}".'
        # Define la prioridad para la actualización
        prioridad = 'media'
    # Crea una notificación con el mensaje y prioridad determinados
    Notificacion.objects.create(tipo=sender.__name__.lower(), mensaje=mensaje, prioridad=prioridad)

# Define un receptor de señal para cuando se elimina un objeto Software o Hardware
@receiver(post_delete, sender=Software)
@receiver(post_delete, sender=Hardware)
def crear_notificacion_eliminacion(sender, instance, **kwargs):
    # Crea un mensaje para la notificación de eliminación
    mensaje = f'Se ha eliminado {sender.__name__.lower()} "{instance.nombre}".'
    # Define la prioridad para la eliminación
    prioridad = 'baja'
    # Crea una notificación con el mensaje y prioridad determinados
    Notificacion.objects.create(tipo=sender.__name__.lower(), mensaje=mensaje, prioridad=prioridad)
