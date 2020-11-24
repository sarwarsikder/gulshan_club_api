from ..models import Event
from rest_framework import generics, permissions
from api.serializer.event_serializers import EventSerializer


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
