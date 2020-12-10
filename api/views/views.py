from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action


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

