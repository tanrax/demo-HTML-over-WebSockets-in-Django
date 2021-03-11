import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from apps.back.models import Post

class BlogConsumer(WebsocketConsumer):

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
        selector = text_data_json["selector"]
        template = text_data_json["template"]
        data = text_data_json["data"]

        # Database
        if template == "partials/blog/all_articles.html":
            data["posts"] = Post.objects.all()[:5]

        if template == "partials/blog/single.html":
            data["post"] = Post.objects.get(data['id'])

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "selector": selector,
                    "html": render_to_string(template, data)
                }
            )
        )