from django.urls import path
from django_webssh.tools.channel import websocket

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]