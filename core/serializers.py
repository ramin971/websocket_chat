from rest_framework import serializers
from .models import ChatMessage,ChatRoom


class ChatMessageSerialzier(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    room = serializers.StringRelatedField()
    class Meta:
        model = ChatMessage
        # fields = ['id','username','room','message','timestamp']
        fields = ['id','room','user','username','message','timestamp']


    def create(self, validated_data):
        room_id = self.context['room_id']
        user = self.context['user']
        return ChatMessage.objects.create(room_id=room_id,user=user,**validated_data)

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'