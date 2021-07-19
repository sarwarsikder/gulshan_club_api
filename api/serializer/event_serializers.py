from django.conf import settings
from rest_framework import serializers
from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        if (obj.image_medium):
            return '%s%s' % (settings.MEDIA_URL, obj.image_medium)

    def get_image_thumbnail(self, obj):
        if (obj.image_thumbnail):
            return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)
    class Meta:
        model = Event
        ordering_fields = ['id', 'created']
        ordering = ['created']
        fields = ('id',
                  'name',
                  'slug',
                  "start_date",
                  "end_date",
                  "url",
                  "description",
                  "image_medium",
                  "image_thumbnail",
                  "image_alt_text",
                  "created")

