from rest_framework import generics, permissions
from ..models import StuffUser
from api.serializer.user_stuff_serializers import UserStuffSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class UserStuffList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = StuffUser.objects.all()
    serializer_class = UserStuffSerializer

class UserStuffDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = StuffUser.objects.all()
    serializer_class = UserStuffSerializer