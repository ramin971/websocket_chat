"""
ASGI config for websocket_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
# import django
# from django.urls import path
# from core import consumers
# from channels.routing import get_default_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from core import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_demo.settings')
# django.setup()
# application = get_default_application()
# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
)
    ),
})