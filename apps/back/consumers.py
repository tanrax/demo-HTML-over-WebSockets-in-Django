import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BlogConsumer(AsyncWebsocketConsumer):

    def connect(self):
        ''' Cliente se conecta '''

        # Recoge el nombre de la sala
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "blog_%s" % self.room_name

        # Se une a la sala
        self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Informa al cliente del éxito
        self.accept()

    def disconnect(self, close_code):
        ''' Cliente se desconecta '''
        # Leave room group
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        ''' Cliente envía información y nosotros la recibimos '''
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        text = text_data_json["text"]

        # Enviamos el mensaje a la sala
        self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "name": name,
                "text": text
            }
        )

    def chat_message(self, event):
        ''' Recibimos información de la sala '''
        name = event["name"]
        text = event["text"]

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "name": name,
                    "text": text
                }
            )
        )
