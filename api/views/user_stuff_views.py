from rest_framework import generics, permissions
from ..models import StuffUser
from api.serializer.user_stuff_serializers import UserStuffSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action, permission_classes, authentication_classes
from api.filter.filters import UserStuffFilter
from django.http import HttpResponse, JsonResponse
from http import HTTPStatus
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters



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
                user_data = UserStuffSerializer(StuffUser.objects.filter(stuff_name__contains=request.GET.get('stuff_name')), many=True).data
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