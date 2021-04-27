from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import generics, permissions
from django.db.models import Q
from django.contrib.auth.hashers import make_password



from api.serializer.user_serializers import UserSerializer, GroupSerializer , UserCategorySerializer
from api.service import paginator_service
from api.models import UserCategory

User = get_user_model()

from rest_framework.decorators import action, permission_classes
from django.http import JsonResponse
import xmltodict
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from http import HTTPStatus
from api.service.sms_service import SmsWireless
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
import random
import json

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
 
from pyexcel_xlsx import get_data

from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from openpyxl import load_workbook
from io import BytesIO
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.conf import settings
import os
from re import search
from PIL import Image






class UserList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all().filter()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name"]
    parser_classes = (MultiPartParser,)


    @action(detail=False, methods=['get'], url_path='user_search')
    def user_search(self, request):
        try:
            if request.user.is_authenticated:
                user_list = User.objects.all()
                search_string = request.GET.get('member_name')
                # user_filter = User.objects.filter(
                #     Q(first_name=search_string) | Q(last_name=search_string),
                # )

                user_filter = User.objects.filter(
                    status=True) & User.objects.filter(first_name__contains=search_string) | User.objects.filter(
                    last_name__contains=search_string) | User.objects.filter(
                    username__contains=search_string) | User.objects.filter(
                    phone_primary__contains=search_string) | User.objects.filter(
                    club_ac_number__contains=search_string)

                print(user_filter)
                # user_data = UserSerializer(instance=user_filter, many=True).data
                user_data = UserSerializer(user_filter, many=True).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='active_user_search')
    def active_user_search(self, request):
        try:
            if request.user.is_authenticated:
                user_list = User.objects.all()
                search_string = request.GET.get('member_name')
                # user_filter = User.objects.filter(
                #     Q(first_name=search_string) | Q(last_name=search_string),
                # )
                print('Inactive User')
                user_filter = User.objects.filter(
                    Q(is_active=True) & (Q(first_name__contains=search_string) |
                                          Q(last_name__contains=search_string) |
                                          Q(username__contains=search_string) |
                                          Q(phone_primary__contains=search_string))

                )

                print(user_filter.query)
                # user_data = UserSerializer(instance=user_filter, many=True).data
                user_data = UserSerializer(user_filter, many=True).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='inactive_user_search')
    def inactive_user_search(self, request):
        try:
            if request.user.is_authenticated:
                user_list = User.objects.all()
                search_string = request.GET.get('member_name')
                # user_filter = User.objects.filter(
                #     Q(first_name=search_string) | Q(last_name=search_string),
                # )
                print('Inactive User')
                user_filter = User.objects.filter(
                    Q(is_active=False) & (Q(first_name__contains=search_string) |
                    Q(last_name__contains=search_string) |
                    Q(username__contains=search_string) |
                    Q(phone_primary__contains=search_string))

                )

                print(user_filter.query)
                # user_data = UserSerializer(instance=user_filter, many=True).data
                user_data = UserSerializer(user_filter, many=True).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='basic_info')
    def user_basic_info(self, request, ):
        try:
            print(request.user)
            if request.user.is_authenticated:
                user = request.user
                user_data = UserSerializer(user).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e) + "Exception")
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='(?P<phone>[\w-]+)/get_opt', permission_classes=[])
    def get_opt_by_phone_number(self, request, phone):
        try:
            if request.user:
                opt = random.randint(1000, 9999)
                opt_message = "Verification code is {0}".format(opt)
                smsWireless = SmsWireless(phone, opt_message)
                response = smsWireless.sendSMSWithGet()

                sms_obj = xmltodict.parse(response)

                request.user.opt = opt
                request.user.save()

                return JsonResponse(
                    {'status': True, 'data': request.user.phone_primary, 'sms_response': sms_obj, 'opt': str(opt)},
                    status=HTTPStatus.OK)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Please submit valid User."
            print(str(e) + "Exception")
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='(?P<opt>[\w-]+)/opt_validate', permission_classes=[])
    def get_opt_validate(self, request, opt):
        try:
            if request.user:
                query_set = User.objects.filter(opt=opt)
                if query_set.exists() > 0:
                    user_data = UserSerializer(query_set[0]).data
                    return JsonResponse(
                        {'status': True, 'data': "Successfully verified"},
                        status=HTTPStatus.OK)
                else:
                    message = "Please submit valid Verification CODE."
                    return JsonResponse(
                        {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Please submit valid User."
            print(str(e) + "Exception")
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='(?P<username>[\w-]+)/phone')
    def get_phone_by_username(self, request, username):
        try:
            query_set = User.objects.filter(username=username)
            if query_set.exists() > 0:
                response = {'status': False, 'message': ''}
                user_data = UserSerializer(query_set[0]).data
                return JsonResponse(
                    {'status': True, 'data': user_data['phone_primary'], 'sms': response}, status=HTTPStatus.OK)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Some thing went wrong."
            print(str(e))
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='inactive-users')
    def get_inactive_user(self, request):
        try:
            if request.user.is_authenticated:
                results = []
                user_list = User.objects.filter(is_active=False)
                paginator = Paginator(user_list, 10)
                page = request.GET.get('page', 1)
                try:
                    user_list = paginator.page(page)
                except PageNotAnInteger:
                    user_list = paginator.page(1)
                except EmptyPage:
                    user_list = paginator.page(paginator.num_pages)

                user_data = UserSerializer(user_list, many=True).data
                #results.append(user_data)

                return paginator_service.response_paginated_user(user_list, user_data, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
    
    @action(detail=False, methods=['post'], url_path='upload-users')
    def  user_upload(self, request):
        try:
            if request.user.is_authenticated:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                excel_file = request.FILES["excel_file"]
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                uploaded_file_url = fs.path(filename)
                #df = pd.read_excel(FILES_DIR+ "" + uploaded_file_url)
                FILES_DIR = os.path.abspath(uploaded_file_url)
                MEDIA_ROOT = settings.MEDIA_ROOT
                # image.save(imagefile,’JPEG’, quality=90)
                df = pd.read_excel(open(FILES_DIR, 'rb'), sheet_name='GridViewExport')
                for i, row in df.iterrows():

                    try:
                        user_username = User.objects.filter(username=str(row['Account']))
                        user_email = User.objects.filter(email=row['E-mail'])
                        substring = '.'
                        category = str(row['Category'])
                        category_obj = UserCategory.objects.filter(category_name=str(category))
                        if category_obj.exists():
                            user_category_data = UserCategorySerializer(category_obj[0]).data
                            user_category_obj = UserCategory.objects.get(pk=user_category_data['id'])

                        mobile = str(row['Mobile'])
                        if search(substring, mobile):
                            mobile = mobile.split(substring)
                            mobile = mobile[0]
                            print(mobile)
                                
                        if user_username.exists():
                            user_username.phone_primary = mobile
                            user_username.update()
                        else:
                            userObj = User()
                            userObj.username = str(row['Account'])

                           
                            full_name = str(row['Members Name'])
                            full_name = full_name.split(" ", 1)
                            userObj.first_name = full_name[0]
                            userObj.last_name = full_name[1]

                            substring = ' '
                            
                            userObj.password = make_password('!@#$1234')
                            email = str(row['E-mail'])
                            substring = ';'
                            if search(substring, email):
                                email = email.split(substring)
                                email = email[0]

                            userObj.email = email
                            userObj.phone_primary = mobile

                            # userObj.status = str(row['Member Status'])
                            userObj.status = 'active'


                            if category_obj.exists():
                                userObj.category_name = user_category_obj

                            if fs.exists(MEDIA_ROOT+'/member_user/medium/'+ row['Account'] +'.JPG'):
                                userObj.image_medium = 'member_user/medium/'+ row['Account'] +'.JPG'

                            if fs.exists(MEDIA_ROOT+'/member_user/thumbnail/'+ row['Account'] +'.JPG'):
                                userObj.image_thumbnail = 'member_user/thumbnail/'+ row['Account'] +'.JPG'
                            userObj.save()
                    except Exception as err:
                        print("An exception occurred" + str(err))
                message = "TEst"
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.OK)
        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='active-users')
    def get_active_user(self, request):
        try:
            if request.user.is_authenticated:
                results = []
                user_list = User.objects.filter(is_active=True)
                paginator = Paginator(user_list, 10)
                page = request.GET.get('page', 1)
                try:
                    user_list = paginator.page(page)
                except PageNotAnInteger:
                    user_list = paginator.page(1)
                except EmptyPage:
                    user_list = paginator.page(paginator.num_pages)

                user_data = UserSerializer(user_list, many=True).data
                results.append(user_data)

                return paginator_service.response_paginated_user(user_list, user_data, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
            
    @action(detail=False, methods=['get'], url_path='active-bod-users')
    def get_active_bod_user(self, request):
        try:
            if request.user.is_authenticated:
                results = []
                user_list = User.objects.filter(status='doard_director')
                paginator = Paginator(user_list, 10)
                page = request.GET.get('page', 1)
                try:
                    user_list = paginator.page(page)
                except PageNotAnInteger:
                    user_list = paginator.page(1)
                except EmptyPage:
                    user_list = paginator.page(paginator.num_pages)

                user_data = UserSerializer(user_list, many=True).data
                results.append(user_data)

                return paginator_service.response_paginated_user(user_list, user_data, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
    
    @action(detail=False, methods=['get'], url_path='active-bod-users-search')
    def inactive_user_search(self, request):
        try:
            if request.user.is_authenticated:
                user_list = User.objects.all()
                search_string = request.GET.get('member_name')
                # user_filter = User.objects.filter(
                #     Q(first_name=search_string) | Q(last_name=search_string),
                # )
                print('Inactive User')
                user_filter = User.objects.filter(
                    Q(status='doard_director') & (Q(first_name__contains=search_string) |
                    Q(last_name__contains=search_string) |
                    Q(username__contains=search_string) |
                    Q(club_ac_number__contains=search_string) |
                    Q(phone_primary__contains=search_string))

                )

                print(user_filter.query)
                # user_data = UserSerializer(instance=user_filter, many=True).data
                user_data = UserSerializer(user_filter, many=True).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)


class UserByUsernameList(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'], url_path='(?P<phone>[\w-]+)/get_opt')
    @permission_classes(([permissions.IsAuthenticated]), )
    def get_opt_by_phone_number(self, request, phone):
        try:
            if request.user:
                return JsonResponse(
                    {'status': True, 'data': request.user.phone_primary}, status=HTTPStatus.OK)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Please submit valid User."
            print(str(e) + "Exception")
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='(?P<username>[\w-]+)/phone')
    def get_phone_by_username(self, request, username):
        try:
            query_set = User.objects.filter(username=username)
            if query_set.exists() > 0:
                response = {'status': False, 'message': ''}
                user_data = UserSerializer(query_set[0]).data
                return JsonResponse(
                    {'status': True, 'data': user_data['phone_primary'], 'sms': response}, status=HTTPStatus.OK)
            else:
                message = "Please submit valid User."
                return JsonResponse(
                    {'status': True, 'data': message}, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            message = "Some thing went wrong."
            print(str(e))
            return JsonResponse(
                {'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
