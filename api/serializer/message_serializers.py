from rest_framework import serializers
from api.serializer.user_serializers import UserSerializer
from  ..models import MessageUser

class UserMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = MessageUser
        fields = ('id','subject', 'sender', 'recipient', 'parent_msg', 'sent_at', 'read_at', 'replied_at')
