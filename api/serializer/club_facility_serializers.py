from rest_framework import serializers
from ..models import ClubFacility


class ClubFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubFacility
        fields = ('id',
                  'name',
                  'description',
                   "image_medium","image_thumbnail")

