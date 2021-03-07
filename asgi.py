import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from channels.routing import ProtocolTypeRouter


application = ProtocolTypeRouter({})
