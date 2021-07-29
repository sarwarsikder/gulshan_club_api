from rest_framework import serializers
from  ..models import Reservation
from api.serializer.user_serializers import UserSerializer
from api.serializer.club_facility_detail_serializers import ClubFacilityDetailSerializer


class ReservationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    facility = ClubFacilityDetailSerializer(read_only=True)
    class Meta:
        model = Reservation
        ordering_fields = ['id']
        ordering = ['id']
        fields = ('id','created_by', 'facility', 'reservation_datetime', 'status', 'created_at','updated_at')