from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Chat, Group

class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Websocket connected...')
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)
        self.group_name= self.scope['url_route']['kwargs']['groupname']
        print("Group Name:", self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()


    async def receive_json(self, content, **kwargs):
        print('Message receive from client', content)
        #find group object
        group= await database_sync_to_async(Group.object.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat= Chat(
                content['msg'],
                group= group
            )
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    type: 'chat.message',
                    'message': content['msg']
                }
            )
        else:
            await self.send_json({
                'message' : 'Login Required'
            })
    async def chat_message(self, event):
        print('Event', event)
        await self.send_json({
            'message':event['message']
        })

    async def disconnect(self, close_code):
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    
        