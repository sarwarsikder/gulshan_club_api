from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import generics, permissions

from api.serializer.user_serializers import UserSerializer, GroupSerializer
from api.service import paginator_service

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


class UserList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all().filter()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name"]

    @action(detail=False, methods=['get'], url_path='user_search')
    def user_search(self, request):
        try:
            if request.user.is_authenticated:
                user_list = User.objects.all()
                search_string = request.GET.get('member_name')
                # user_filter = User.objects.filter(
                #     Q(first_name=search_string) | Q(last_name=search_string),
                # )

                user_filter = User.objects.filter(first_name__contains=search_string) | User.objects.filter(
                    last_name__contains=search_string) | User.objects.filter(
                    username__contains=search_string) | User.objects.filter(
                    phone_primary__contains=search_string)

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
                user_list = User.objects.filter(status="inactive")
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

                return paginator_service.response_paginated(user_list, results, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['get'], url_path='active-users')
    def get_active_user(self, request):
        try:
            if request.user.is_authenticated:
                results = []
                user_list = User.objects.filter(status="active")
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

                return paginator_service.response_paginated(user_list, results, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
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
