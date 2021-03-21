import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from apps.back.models import Post, Comment

class BlogConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
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
            # Set data
            data["post"] = Post.objects.get(pk=data['id'])
            data["comments"] = Comment.objects.filter(post__id=data['id']).order_by("-created_on").all()
            # Add new comment
            data["newName"] = data['newName'] if 'newName' in data else ''
            data["newMessage"] = data['newMessage'] if 'newMessage' in data else ''
            newComment = 'newComment' in data
            # Validation
            error = (len(data["newName"]) == 0 or len(data["newMessage"]) == 0) and newComment
            data["error"] = error
            if newComment and not error:
                # Insert
                Comment(
                    name=data["newName"],
                    body=data["newMessage"],
                    post=Post.objects.get(pk=data['id'])
                ).save()
                # Clean form
                data["newName"] = ''
                data["newMessage"] = ''

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "selector": selector,
                    "html": render_to_string(template, data)
                }
            )
        )
