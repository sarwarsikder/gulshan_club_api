from http import HTTPStatus

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, permissions
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from api.serializer.user_stuff_serializers import UserStuffSerializer
from ..models import StuffUser


class UserStuffList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = StuffUser.objects.all().filter()
    serializer_class = UserStuffSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["stuff_name"]

    @action(detail=False, methods=['get'], url_path='stuff_search')
    def user_search(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                user_filter = StuffUser.objects.filter(stuff_name__contains=request.GET.get('stuff_name')) | StuffUser.objects.filter(
                    designation__contains=request.GET.get('stuff_name')) |  StuffUser.objects.filter(
                    designation_group__contains=request.GET.get('stuff_name')).order_by('-id')

                user_data = UserStuffSerializer(user_filter, many=True).data
                return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.ACCEPTED)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)


class UserStuffDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = StuffUser.objects.all()
    serializer_class = UserStuffSerializer
