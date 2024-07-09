"""
ASGI config for Email project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from mail.routing import websocket_urlpatterns  # Импортируйте ваши WebSocket маршруты

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')  # Замените на имя вашего проекта

application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # Обработка HTTP запросов
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),  # Обработка WebSocket запросов
})

