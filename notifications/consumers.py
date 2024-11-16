import json  # Para manejar la serialización y deserialización de datos en formato JSON.
from channels.generic.websocket import AsyncWebsocketConsumer  # Clase base para consumidores WebSocket asíncronos en Django Channels.

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Se llama cuando un cliente intenta establecer una conexión WebSocket.
        Se une al grupo de notificaciones para recibir mensajes.
        """
        self.room_group_name = 'notificaciones'  # Define el grupo al que se unirá este consumidor.
        # Unirse al grupo de la sala.
        await self.channel_layer.group_add(
            self.room_group_name,  # Nombre del grupo.
            self.channel_name  # Nombre del canal único para esta conexión.)
        # Aceptar la conexión WebSocket.
        await self.accept()

    async def disconnect(self, close_code):
        """
        Se llama cuando la conexión WebSocket se cierra.
        Se sale del grupo de notificaciones.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,  # Nombre del grupo del que se saldrá.
            self.channel_name ) # Nombre del canal del consumidor.

    async def notificacion_message(self, event):
        """
        Se llama cuando se envía un mensaje de notificación al grupo de la sala.
        Envía el mensaje de notificación al cliente a través del WebSocket.
        """
        mensaje = event['mensaje']  # Extraer el mensaje del evento.
        # Enviar el mensaje de notificación al cliente.
        await self.send(text_data=json.dumps({
            'mensaje': mensaje}))  # Incluir el mensaje en el JSON que se envía.