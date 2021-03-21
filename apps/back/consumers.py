import json
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from apps.back.models import Post, Comment
from asgiref.sync import async_to_sync

class BlogConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "blog"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        pass

    def receive(self, text_data):
        send = False
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
                # Send Broadcast
                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            "type": "blog.new.comment",
                            "text": {
                                "selector": selector,
                                "template": template,
                                "html": render_to_string(template, data)
                            }
                        })
                send = True

        # Send message to WebSocket
        if not send:
            self.send(
                text_data=json.dumps(
                    {
                        "selector": selector,
                        "template": template,
                        "html": render_to_string(template, data)
                    }
                )
            )

    def blog_new_comment(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "selector": event["text"]["selector"],
                    "template": event["text"]["template"],
                    "html": event["text"]["html"]
                }
            )
        )
