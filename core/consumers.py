import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom,ChatMessage
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print('!!!!!!',self.scope)
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        print('$$$querystring: ',query_string)
        if query_string:
            params = dict(param.split('=') for param in query_string.split('&'))
            print('####params:',params)

            access_token = params.get('token')
        # headers = dict(self.scope.get('headers', []))
        print('####access:',access_token)
        # print('####headers-token:',headers.get(b'authorization', b''))
        # access_token = headers.get(b'authorization', b'').decode('utf-8').split(' ')[1]
        # self.room_name = "chat_room"
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print('##########room_name: ',self.room_name)
        # print('access*************: ',access_token)
        # Join room group
        user = await self.get_user_from_token(access_token)
        if user:
            self.scope['user'] = user
        else:
            self.scope['user'] = AnonymousUser()

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
        if isinstance(self.scope['user'], AnonymousUser):
            user= None
            username = 'Guest'
            print("####Guest####")
        else:
            user = self.scope['user']
            username = user.username
            # user = await database_sync_to_async(User.objects.get)(username=username)

            print("####user####")
        # username = self.scope['user'].username


        # Get or create the chat room
        room, created = await database_sync_to_async(ChatRoom.objects.get_or_create)(name=self.room_name)
        print('##room_created? ',created)
        # Save the message to the database

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

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        try:
            token = AccessToken(access_token)
            user_id = token['user_id']
            return User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return None