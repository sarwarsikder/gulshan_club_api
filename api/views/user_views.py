from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions
from api.serializer.user_serializers import UserSerializer, GroupSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
User = get_user_model()

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
import json
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserByUsernameList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = UserSerializer
    queryset = User.objects.all()



    @action(detail=False, methods=['get'],url_path='phone/(?P<username>[\w-]+)')
    def get_phone_username(self,request,username):
          return JsonResponse({'status': True, 'data': UserSerializer(User.objects.filter(username=username)[0]).data})


        # print(self.kwargs['username'])
        # obj = get_object_or_404(User, username=self.kwargs['username'])
        # return obj
        # username = self.kwargs['username']
        # return User.objects.filter(username=username)

        
class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer