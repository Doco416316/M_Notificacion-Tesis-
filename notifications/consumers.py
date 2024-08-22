import json  # Importa la librería json para manejar la serialización y deserialización de datos en formato JSON.
from channels.generic.websocket import AsyncWebsocketConsumer  # Importa AsyncWebsocketConsumer, una clase base para consumidores WebSocket asíncronos en Django Channels.

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Este método se llama cuando un cliente intenta establecer una conexión WebSocket.

        # Define el nombre del grupo de la sala al que se unirá este consumidor. 
        # En este caso, todos los consumidores se unen al mismo grupo 'notificaciones'.
        self.room_group_name = 'notificaciones'

        # Unirse al grupo de la sala.
        # Esto permite que el consumidor reciba mensajes enviados al grupo 'notificaciones'.
        await self.channel_layer.group_add(
            self.room_group_name,  # Nombre del grupo.
            self.channel_name  # Nombre del canal del consumidor, único para esta conexión.
        )

        # Aceptar la conexión WebSocket.
        # Si no se llama a este método, la conexión WebSocket será rechazada.
        await self.accept()

    async def disconnect(self, close_code):
        # Este método se llama cuando la conexión WebSocket se cierra.

        # Salirse del grupo de la sala.
        # Esto asegura que el consumidor ya no reciba mensajes enviados al grupo después de desconectarse.
        await self.channel_layer.group_discard(
            self.room_group_name,  # Nombre del grupo del que se saldrá.
            self.channel_name  # Nombre del canal del consumidor.
        )

    async def notificacion_message(self, event):
        # Este método se llama cuando se envía un mensaje de notificación al grupo de la sala.
        # 'event' es un diccionario que contiene el mensaje y otros datos.

        # Extraer el mensaje del evento.
        mensaje = event['mensaje']

        # Enviar el mensaje de notificación al cliente a través del WebSocket.
        # El mensaje se envía como un string en formato JSON.
        await self.send(text_data=json.dumps({
            'mensaje': mensaje  # Incluye el mensaje en el JSON que se envía.
        }))
