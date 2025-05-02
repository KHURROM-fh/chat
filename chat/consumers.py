from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs

class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            # 1. JWT Authentication
            query_params = parse_qs(self.scope['query_string'].decode())
            token = query_params.get('token', [None])[0]
            if not token:
                raise ValueError("Token required")
            
            access_token = AccessToken(token)
            self.scope['user'] = await self.get_user(access_token['user_id'])
            
            # 2. Group Validation
            self.group_name = self.scope['url_route']['kwargs']['groupname']
            if not self.group_name:
                raise ValueError("Group name required")
            
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            await self.close(code=4001)

    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        try:
            message = content.get('msg')
            if not message:
                raise ValueError("Message empty")
                
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': self.scope['user'].username
                }
            )
        except Exception as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        await self.send_json({
            'message': event['message'],
            'sender': event['sender']
        })