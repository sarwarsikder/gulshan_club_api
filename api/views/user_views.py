from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions
from api.serializer.user_serializers import UserSerializer, GroupSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
User = get_user_model()

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes, authentication_classes
from django.http import HttpResponse, JsonResponse
import json
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from http import HTTPStatus
import requests
import urllib

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserByUsernameList(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'], url_path='(?P<phone>[\w-]+)/get_opt')
    @permission_classes(([permissions.IsAuthenticated]), )
    def get_opt_by_phone_number(self, request, phone):
        try:
            if request.user:
                return JsonResponse(
                    {'status': True, 'data': request.user.phone_primary}, status=HTTPStatus.ACCEPTED)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Please submit valid User."
            print(str(e) + "Exception")
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'],url_path='(?P<username>[\w-]+)/phone')
    def get_phone_by_username(self,request,username):
        try:
            query_set = User.objects.filter(username=username)
            if query_set.exists()>0:
                response = {'status': False, 'message': ''}
                user_data = UserSerializer(query_set[0]).data
                print("TEST DATA")
                print(user_data['image'].large)
                print("TEST DATA One")
                # url = 'http://sms.sslwireless.com/pushapi/dynamic/server.php'
                # print(url)
                # headers = {
                #     'Content-Type': 'application/json',
                # }
                #
                # PARAMS = {
                #     'user':'GhulshanClub',
                #     'pass':'62?3b04y',
                #     'sid':'GCLeng',
                #     'msisdn':'+8801713523713',
                #     'sms':'TestSMS1 Test sms2 Test sms API3',
                #     'csmsid':'123456789',
                # }
                #
                # print(PARAMS)
                # print("dsdsd")
                #
                # try:
                #     print(url)
                #     res = requests.get(url=url,params=PARAMS)
                #     print("TEST!")
                #     print(type(res))
                #     print( "dd")
                #     data = res[0].json()
                #     print(data+"TEST")
                #     response['status'] = True
                #     response['data'] = data
                # except Exception as e:
                #     print('ex' + str(e))
                #     response['status'] = False

                return JsonResponse(
                    {'status': True, 'data': user_data['phone_primary'],'sms':response},status=HTTPStatus.ACCEPTED)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message},status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Some thing went wrong."
            print(str(e))
            return JsonResponse(
                {'status': True, 'data':message},status=HTTPStatus.EXPECTATION_FAILED)
        
class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer