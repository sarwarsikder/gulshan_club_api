from rest_framework import serializers
from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
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

