# notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notificaciones'

        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salirse del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notificacion_message(self, event):
        # Enviar mensaje de notificación a través del WebSocket
        mensaje = event['mensaje']

        await self.send(text_data=json.dumps({
            'mensaje': mensaje
        }))
