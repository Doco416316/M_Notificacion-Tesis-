from datetime import timedelta
from django.utils.timezone import now
from software.models import Software  # Asegúrate de que el nombre del modelo sea correcto
from .models import Notificacion

def verificar_software_sin_modificar():
    """
    Verifica los softwares que no han actualizado su licencia en el último año.
    Crea una notificación de alta prioridad para cada software que cumpla con esta condición.
    """
    # Define la fecha de corte para determinar software sin actualizar en más de un año.
    un_ano_atras = now() - timedelta(days=365)
    # Obtiene los softwares cuya última modificación de licencia fue hace más de un año.
    software_sin_modificar = Software.objects.filter(fecha_modificacion_licencia__lte=un_ano_atras)
    # Itera sobre cada software sin modificar para crear una notificación correspondiente.
    for software in software_sin_modificar:
        # Genera el mensaje para la notificación.
        mensaje = f"El software '{software.nombre}' no ha actualizado su licencia en más de un año."
        # Crea la notificación de alta prioridad en la base de datos.
        Notificacion.objects.create(
            mensaje=mensaje,
            prioridad='alta',  # Prioridad establecida como alta para alertas de licencia vencida.
            tipo_cambio='alerta',  # Tipo de cambio 'alerta' para identificar este tipo de notificaciones.
            origen='software',  # Origen definido como software.
            fecha_creacion=now()  # Fecha de creación establecida en el momento actual.
        )
