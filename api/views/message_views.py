import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action

from api.serializer.message_serializers import UserMessageSerializer
from ..models import MessageUser
from ..service import paginator_service

User = get_user_model()


class MessageView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = MessageUser.objects.all().filter()
    serializer_class = UserMessageSerializer

    @action(detail=False, methods=['get'], url_path='inbox')
    def message_inbox(self, request):
        try:
            if request.user.is_authenticated:
                results = []
                message_list = MessageUser.objects.inbox_for(request.user)
                paginator = Paginator(message_list, 10)
                page = request.GET.get('page', 1)
                try:
                    message_list = paginator.page(page)
                except PageNotAnInteger:
                    message_list = paginator.page(1)
                except EmptyPage:
                    message_list = paginator.page(paginator.num_pages)

                for ml in message_list:
                    user_data = UserMessageSerializer(ml).data
                    temp_count = MessageUser.objects.count_unread_message(user=request.user, recipient=ml.sender,
                                                                          max_limit=5)
                    if temp_count >= 5:
                        user_data['count'] = "5+"
                    else:
                        user_data['count'] = str(temp_count)
                        results.append(user_data)

                return paginator_service.response_paginated(message_list, results, request)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['post'], url_path='inbox-details')
    def message_single_user_inbox(self, request):
        try:
            if request.user.is_authenticated:
                parent_id = request.POST.get('parent_id')
                message_list = MessageUser.objects.inbox_for_single_user(request.user, parent_id)
                message_list.update(read_at=datetime.datetime.now())
                # message_list = MessageUser.objects.filter(
                #     recipient=request.user,
                #     recipient_deleted_at__isnull=True,
                # )
                print(message_list)
                user_data = UserMessageSerializer(message_list, many=True)
                print(user_data)
                return JsonResponse(
                    {'status': True, 'data': user_data.data}, status=HTTPStatus.ACCEPTED)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['post'], url_path='select-inbox')
    def select_single_user_inbox(self, request):
        try:
            if request.user.is_authenticated:
                message_list = MessageUser.objects.select_for_single_user(request.user, request.POST.get('recipient'))
                # message_list = MessageUser.objects.filter(
                #     recipient=request.user,
                #     recipient_deleted_at__isnull=True,
                # )
                message_list.update(read_at=datetime.datetime.now())
                print(message_list)
                user_data = UserMessageSerializer(message_list, many=True)
                print(user_data)
                return JsonResponse(
                    {'status': True, 'data': user_data.data}, status=HTTPStatus.ACCEPTED)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

    @action(detail=False, methods=['post'], url_path='compose')
    def message_compose(self, request):
        try:
            if request.user.is_authenticated:
                user_data = {}
                if request.method == "POST":
                    messageUser = MessageUser()
                    sender = request.user
                    subject = request.POST.get('subject')
                    recipient = request.POST.get('recipient')

                    parent_msg = MessageUser.objects.parent_for(request.user, User.objects.get(pk=recipient))
                    if parent_msg.exists() > 0:
                        user_data = UserMessageSerializer(parent_msg[0]).data
                        print(user_data['id'])
                        messageUser.sender = sender
                        messageUser.subject = subject
                        messageUser.recipient = User.objects.get(pk=recipient)
                        messageUser.parent_msg = MessageUser.objects.get(pk=user_data['id'])
                        messageUser.save()
                        user_data = MessageUser.objects.get(id=messageUser.id)
                        user_data = UserMessageSerializer(user_data)
                    else:
                        messageUser.sender = sender
                        messageUser.subject = subject
                        messageUser.recipient = User.objects.get(pk=recipient)
                        messageUser.parent_msg = None
                        messageUser.save()
                        user_data = MessageUser.objects.get(id=messageUser.id)
                        user_data = UserMessageSerializer(user_data)

                    return JsonResponse(
                        {'status': True, 'data': user_data.data}, status=HTTPStatus.ACCEPTED)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
