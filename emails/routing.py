from django.urls import path
from .consumers import EmailConsumer

websocket_urlpatterns = [
    path("ws/email/",EmailConsumer.as_asgi())
]