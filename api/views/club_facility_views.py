from ..models import ClubFacility
from rest_framework import generics, permissions
from api.serializer.club_facility_serializers import ClubFacilitySerializer


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class ClubFacilityList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = ClubFacility.objects.all().order_by('-id')
    serializer_class = ClubFacilitySerializer


class ClubFacilityDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = ClubFacility.objects.all().order_by('-id')
    serializer_class = ClubFacilitySerializer
