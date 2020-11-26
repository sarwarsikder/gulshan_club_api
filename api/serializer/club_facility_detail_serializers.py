from rest_framework import serializers
from ..models import ClubFacilityDetail


class ClubFacilityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubFacilityDetail
        fields = ('id',
                  'name',
                  'club_facility',
                  'description',
                   "image_medium",
                   "image_thumbnail")

