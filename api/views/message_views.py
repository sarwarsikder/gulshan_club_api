from rest_framework import permissions
from api.serializer.message_serializers import UserMessageSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from http import HTTPStatus
from rest_framework import viewsets
from ..models import MessageUser


User = get_user_model()


class MessageView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = MessageUser.objects.all().filter()
    serializer_class = UserMessageSerializer

    @action(detail=False, methods=['get'], url_path='inbox')
    def message_inbox(self, request):
        try:
            if request.user.is_authenticated:
                message_list = MessageUser.objects.inbox_for(request.user)
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

    @action(detail=False, methods=['get'], url_path='(?P<parent_id>[\w-]+)/inbox')
    def message_single_user_inbox(self, request, parent_id):
        try:
            if request.user.is_authenticated:
                message_list = MessageUser.objects.inbox_for_single_user(request.user, parent_id)
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
                    parent_msg = request.POST.get('parent_msg')
                    messageUser.sender = sender
                    messageUser.subject = subject
                    messageUser.recipient = User.objects.get(pk=recipient)
                    messageUser.parent_msg = MessageUser.objects.get(pk=parent_msg)
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
