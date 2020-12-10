from rest_framework import serializers
from ..models import StuffUser
from django.conf import settings



class UserStuffSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        if (obj.image_medium):
            return '%s%s' % (settings.MEDIA_URL, obj.image_medium)

    def get_image_thumbnail(self, obj):
        if (obj.image_thumbnail):
            return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)

    class Meta:
        model = StuffUser
        fields = ('id','stuff_name', 'designation_group', "designation", "mobile_number_primary","image_medium","image_thumbnail")