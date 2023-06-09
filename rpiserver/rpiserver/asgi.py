"""
ASGI config for rpiserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from CameraSite.routing import websocket_urlpatterns

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpiserver.settings")

# django.setup()
# import chat.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "https": django_asgi_app,
        "websocket": 
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

