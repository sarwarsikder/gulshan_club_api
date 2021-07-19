from django.conf import settings
from rest_framework import serializers
from ..models import ClubFacilityDetail


class ClubFacilityDetailSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        if (obj.image_medium):
            return '%s%s' % (settings.MEDIA_URL, obj.image_medium)

    def get_image_thumbnail(self, obj):
        if (obj.image_thumbnail):
            return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)

    class Meta:
        model = ClubFacilityDetail
        ordering_fields = ['id', 'created_at']
        ordering = ['id']
        fields = ('id',
                  'name',
                  'club_facility',
                  'description',
                   "image_medium",
                   "image_thumbnail",
                   'created_at')

