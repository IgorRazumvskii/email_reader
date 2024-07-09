from django.urls import path
from .consumers import EmailFetchConsumer

websocket_urlpatterns = [
    path('ws/fetch-emails/', EmailFetchConsumer.as_asgi()),
]