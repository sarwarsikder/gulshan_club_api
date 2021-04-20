from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action



# function based views.py
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
# other decorators if required
@permission_classes([IsAuthenticated])
def user_create(request):
    user_data = 'test'
    return JsonResponse(
                    {'status': True, 'data': user_data}, status=HTTPStatus.OK)



class StoreManager(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='store_factory_manager')
    def store_manager_factory(self,request):
        try:
            return JsonResponse(
                    {'status': True, 'data': "Store enabled successfully"}, status=HTTPStatus.OK)

        except Exception as e:
            message = "Please submit valid User."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

