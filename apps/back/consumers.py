import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from apps.back.models import Post, Comment

class BlogConsumer(WebsocketConsumer):

    def connect(self):
        ''' Cliente se conecta '''
        self.accept()

    def disconnect(self, close_code):
        ''' Cliente se desconecta '''
        pass

    def receive(self, text_data):
        ''' Cliente envía información y nosotros la recibimos '''
        text_data_json = json.loads(text_data)
        selector = text_data_json["selector"]
        template = text_data_json["template"]
        data = text_data_json["data"]

        # Database
        if template == "partials/blog/all_articles.html":
            pag = data['pag'] if 'pag' in data else 1
            amount = 3
            start = pag - 1
            end = start + amount
            data["posts"] = Post.objects.all()[start:end]
            data['pag'] = pag

        if template == "partials/blog/single.html":
            data["post"] = Post.objects.get(pk=data['id'])
            data["comments"] = Comment.objects.filter(post__id=data['id']).all()

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "selector": selector,
                    "html": render_to_string(template, data)
                }
            )
        )