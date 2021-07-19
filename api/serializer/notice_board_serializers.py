from rest_framework import serializers
from  ..models import NoticeBoard

class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        ordering_fields = ['id', 'created_at']
        ordering = ['created_at']
        fields = ('id', 'title', 'message', 'tag', 'image_medium', 'image_thumbnail', 'created_at', 'updated_at')
