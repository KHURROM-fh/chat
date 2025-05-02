from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ajws/<str:groupname>', consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]
