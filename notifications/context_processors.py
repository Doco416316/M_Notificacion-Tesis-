# notificaciones/context_processors.py
from .models import Notificacion

def unread_notifications(request):
    unread_notifications_count = Notificacion.objects.filter(leido=False).count()
    return {'unread_notifications_count': unread_notifications_count}
