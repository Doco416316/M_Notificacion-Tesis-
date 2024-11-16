from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notificaciones/', consumers.NotificacionesConsumer.as_asgi()),
]
