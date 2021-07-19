from ..models import ClubFacilityDetail
from rest_framework import generics, permissions
from api.serializer.club_facility_detail_serializers import ClubFacilityDetailSerializer


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class ClubFacilityDeailsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = ClubFacilityDetail.objects.all().order_by('-id')
    serializer_class = ClubFacilityDetailSerializer


class ClubFacilityDetailDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = ClubFacilityDetail.objects.all().order_by('-id')
    serializer_class = ClubFacilityDetailSerializer
