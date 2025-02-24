from rest_framework import viewsets
from .models import ChatMessage,ChatRoom
from .serializers import ChatMessageSerialzier,ChatRoomSerializer
from django.shortcuts import render



class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerialzier
    # lookup_field = 'room__name'

    def get_queryset(self):
        # room_name = self.kwargs['room__name']
        # print('*********',room_id)
        # return ChatMessage.objects.filter(room__name=room_name)
        return ChatMessage.objects.filter(room_id=self.kwargs['room_pk'])

    def get_serializer_context(self):
        # room_id = ChatRoom.objects.get(name=self.kwargs['room__name']).id
        print('#########user :',self.request.user)
        # return {'room_id':room_id}
        return {'room_id':self.kwargs['room_pk'], 'user':self.request.user}


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


def chat_test(request,room_name):
    # token = str(request.query_params.get('token',None))
    token = request.GET.get('token',None)
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMjQ0NjQ2LCJpYXQiOjE3NDAyMzAyNDYsImp0aSI6IjhkM2JjZDhiNzY3YzRhODZhMTc1NDZhOTg0MDg0NDA0IiwidXNlcl9pZCI6MX0.1KTVTwviAaSdV4VAuJVYI1eVmOUj-LOlKTKphrcfbJU"
    # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMjQwMzI1LCJpYXQiOjE3NDAyMjU5MjUsImp0aSI6IjQzYWQ1YTczZmE0OTQ0ZmQ5ZDgyMzUwODY4ZmRjNTEyIiwidXNlcl9pZCI6Mn0.3572JeYI8VJitoqlFvvXQU6k1ualdVGFi9DACmKAmiw'
    return render(request, 'chat_test.html',{'room_name':room_name, 'token':token})