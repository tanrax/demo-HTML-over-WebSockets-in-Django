import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_demo.settings")
import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.back.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
