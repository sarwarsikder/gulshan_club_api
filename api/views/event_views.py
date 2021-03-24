from ..models import Event
from rest_framework import generics, permissions
from api.serializer.event_serializers import EventSerializer
from rest_framework.response import Response
import datetime


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class EventList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        if 'year' in request.GET and request.GET['year']:
            print("TEST")
            start_year =  request.GET['year'] + '-01-01'
            print(start_year)
            end_year =  request.GET['year'] + '-12-31'
            print(end_year)
            queryset = Event.objects.all().filter(start_date__range=[start_year,end_year])
            serializer = EventSerializer(queryset, many=True)
        else:
            serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

class EventDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
