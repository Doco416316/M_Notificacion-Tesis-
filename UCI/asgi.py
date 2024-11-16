"""
ASGI config for UCI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notificaciones.routing import websocket_urlpatterns  # importas las rutas WebSocket de tu app
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UCI.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Maneja peticiones HTTP de la misma manera que ASGI tradicional
    "websocket": AuthMiddlewareStack(  # WebSocket, usa middleware para autenticación
        URLRouter(
            websocket_urlpatterns  # Ruta de WebSocket configurada
        )
    ),
})


