from rest_framework import serializers
from  ..models import NoticeBoard

class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = ('title', 'message', 'tag', 'created_at', 'updated_at')
