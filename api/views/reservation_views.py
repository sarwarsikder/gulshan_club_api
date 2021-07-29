from rest_framework.decorators import action, permission_classes, api_view, authentication_classes
from http import HTTPStatus
from django.http import HttpResponse, JsonResponse
import json
from api.models import Reservation,ClubFacilityDetail
from django.contrib.auth import get_user_model
User = get_user_model()
import dateutil.parser
from django.utils.dateparse import parse_date 
import datetime
from django.core.paginator import Paginator
from api.service import paginator_service
from api.serializer.reservation_serializers import ReservationSerializer





@api_view(['POST'])
def post_reservation(request):
        try:
            if request.user.is_authenticated:
                if request.method == 'POST':
                    json_data = json.dumps(request.data)
                    body_data = json.loads(json_data)
                    
                    facility_id = body_data['facility_id']
                    facility = ClubFacilityDetail.objects.get(id=facility_id)
                    
                  
                    observation_date = datetime.datetime.strptime(body_data['observation_date'], "%Y-%m-%d %H:%M")
                    
                    
                    reservation = Reservation()
                    reservation.facility = facility
                    reservation.created_by = request.user
                    reservation.reservation_date = observation_date
                    reservation.save()
                    
                    return JsonResponse({'status': True, 'message': 'Your reservation has been post,We will contact you shortly.'}, status=HTTPStatus.OK)
            else:
                message = "User is not valid."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong." + str(e)
            return JsonResponse({'status': True, 'message': message}, status=HTTPStatus.EXPECTATION_FAILED)
        
@api_view(['GET'])
def get_observation(request,status='all'):
        try:
            if request.user.is_authenticated:
                
                if status == 'all':
                    payment_list = Reservation.objects.filter(created_by=request.user).order_by('-id')
                elif status == 'pending':
                     payment_list = Reservation.objects.filter(created_by=request.user, status = "Pending").order_by('-id')
                elif status == 'confirmed':
                     payment_list = Reservation.objects.filter(created_by=request.user, status = "Confirmed").order_by('-id')
                elif status == 'canceled':
                     payment_list = Reservation.objects.filter(created_by=request.user, status = "Canceled").order_by('-id')
                else:
                     payment_list = Reservation.objects.filter(created_by=request.user).order_by('-id')
               

                results = []
                paginator = Paginator(payment_list, 10)
                page = request.GET.get('page', 1)
                try:
                    payment_list = paginator.page(page)
                except PageNotAnInteger:
                    payment_list = paginator.page(1)
                except EmptyPage:
                    payment_list = paginator.page(paginator.num_pages)

                user_payment_filter = ReservationSerializer(payment_list, many=True).data
                results.append(user_payment_filter)
                message = "Observation fetch successfully."

                return paginator_service.response_paginated(payment_list, user_payment_filter, request)
            else:
                message = "User not valid!"
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)