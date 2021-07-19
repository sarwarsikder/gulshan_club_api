from rest_framework import serializers
from django.conf import settings
from  ..models import NoticeBoard

class NoticeBoardSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        if (obj.image_medium):
            return '%s%s' % (settings.MEDIA_URL, obj.image_medium)

    def get_image_thumbnail(self, obj):
        if (obj.image_thumbnail):
            return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)
    class Meta:
        model = NoticeBoard
        ordering_fields = ['id', 'created_at']
        ordering = ['created_at']
        fields = ('id', 'title', 'message', 'tag', 'image_medium', 'image_thumbnail', 'created_at', 'updated_at')
