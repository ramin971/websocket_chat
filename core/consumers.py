import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom,ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "chat_room"
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print('##########room_name: ',self.room_name)
        # print('scop*************: ',self.scope)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            # "chat_group",
            # self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            # "chat_group",
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('######receive##########')
        print('####message: ####',message)
        print('***user***: ',self.scope['user'])
        username = self.scope['user'].username


        # Get or create the chat room
        room, created = await database_sync_to_async(ChatRoom.objects.get_or_create)(name=self.room_name)
        print('##room_created? ',created)
        # Save the message to the database
        user = await database_sync_to_async(User.objects.get)(username=username)
        chat_message = ChatMessage(room=room,user=user,message=message)
        # chat_message = ChatMessage(message=message)
        await database_sync_to_async(chat_message.save)()
        print('*******chat_save*******')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            # "chat_group",
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
    
    async def chat_message(self,event):
        message = event['message']
        print('########3 message:',message)
        username = event['username']

        # Send message to websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))