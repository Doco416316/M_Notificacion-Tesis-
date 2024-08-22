# Importa las señales post_save y post_delete de Django, que se activan después de guardar o eliminar una instancia del modelo
from django.db.models.signals import post_save, post_delete
# Importa el decorador receiver, que se usa para conectar las señales con las funciones receptoras
from django.dispatch import receiver
# Importa el modelo Notificacion desde la aplicación notifications
from notifications.models import Notificacion
# Importa el modelo Hardware desde la aplicación hardware
from hardware.models import Hardware

# Define una función receptora que se ejecuta después de que se guarda una instancia del modelo Hardware
@receiver(post_save, sender=Hardware)
def crear_notificacion_cambio_hardware(sender, instance, created, **kwargs):
    # Verifica si la instancia de Hardware fue creada o actualizada
    if created:
        # Si se creó, define el mensaje y la prioridad para la notificación de creación
        mensaje = f'Se ha agregado hardware "{instance.nombre}".'
        prioridad = 'alta'  # Asigna una prioridad alta para la creación de hardware
    else:
        # Si se actualizó, define el mensaje y la prioridad para la notificación de actualización
        mensaje = f'Se ha actualizado hardware "{instance.nombre}".'
        prioridad = 'media'  # Asigna una prioridad media para la actualización de hardware

    # Crea una nueva notificación en la base de datos con el tipo, mensaje, y prioridad especificados
    Notificacion.objects.create(tipo='hardware', mensaje=mensaje, prioridad=prioridad)

# Define una función receptora que se ejecuta después de que se elimina una instancia del modelo Hardware
@receiver(post_delete, sender=Hardware)
def crear_notificacion_eliminacion_hardware(sender, instance, **kwargs):
    # Define el mensaje para la notificación de eliminación de hardware
    mensaje = f'Se ha eliminado hardware "{instance.nombre}".'

    # Crea una nueva notificación en la base de datos con el tipo 'hardware', el mensaje, y una prioridad baja
    Notificacion.objects.create(tipo='hardware', mensaje=mensaje, prioridad='baja')
