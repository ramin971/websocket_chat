from rest_framework import serializers
from .models import ChatMessage,ChatRoom
from django.contrib.auth.models import AnonymousUser



class ChatMessageSerialzier(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    room = serializers.StringRelatedField()
    class Meta:
        model = ChatMessage
        # fields = ['id','username','room','message','timestamp']
        fields = ['id','room','username','message','timestamp']


    def create(self, validated_data):
        room_id = self.context['room_id']
        user = self.context['user']
        if isinstance(user, AnonymousUser):
            print('user#### ',user)
            user = None
        return ChatMessage.objects.create(room_id=room_id,user=user,**validated_data)

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'