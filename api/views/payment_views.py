
from rest_framework import viewsets, filters
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import generics, permissions
from rest_framework.decorators import action, permission_classes, api_view
from django.http import JsonResponse
from http import HTTPStatus

from api.models import PostPayment
from api.serializer.payment_serializers import PaymentSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.paginator import Paginator

from api.service.city_bank_service import PaymentsCityBank
from api.service import paginator_service


import os
from django.conf import settings
import json, xmltodict
import  xml.etree 


@api_view(['POST'])
def  city_bank_payment(request):
        try:
            if request.user.is_authenticated:
                    if request.method == 'POST':
                        print(request.POST['amount'])

                        amount = str(request.POST['amount'])
                        reference_number = str(request.POST['reference'])

                        if not amount:
                            message = 'Write valid ammount'
                            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

                        proxy =""
                        proxyauth =""
                        postDatatoken = '{"password": "123456Aa","userName": "test"}'
                        serviceUrltoken =""
                        serviceUrltoken= 'https://sandbox.thecitybank.com:7788/transaction/token'
                        cblcz = PaymentsCityBank(postDatatoken,serviceUrltoken,proxy,proxyauth)
                        
                        transaction = cblcz.executePayment()    
                        transaction_json = json.loads(transaction)
                        
                        transactionId = transaction_json['transactionId']
                        
                        declined = settings.BASE_URL+"api/v1/payments/city-declined/"
                        approved = settings.BASE_URL+"api/v1/payments/city-approved/"
                        cancelled = settings.BASE_URL+"api/v1/payments/city-cancelled/"
                    
                        postdataEcomm = '{"merchantId": "11122333","amount": "'+amount+'","currency": "050","description": "'+reference_number+'","approveUrl": "'+approved+'","cancelUrl": "'+cancelled+'","declineUrl": "'+declined+'","userName": "test","passWord": "123456Aa","secureToken": "'+ transactionId +'"}'
                        serviceUrlEcomm = 'https://sandbox.thecitybank.com:7788/transaction/createorder'
                        
                        cblEcomm = PaymentsCityBank(postdataEcomm,serviceUrlEcomm,proxy,proxyauth)
                        cblEcomm = cblEcomm.executePayment()    
                        cblEcomm_json = json.loads(cblEcomm)

                        orderId = cblEcomm_json['items']['orderId']
                        sessionId = cblEcomm_json['items']['sessionId']
                        url = cblEcomm_json['items']['url']

                        redirectUrl = url+"?ORDERID="+orderId+"&SESSIONID="+sessionId
                        return JsonResponse({'status': True, 'pay_url': redirectUrl}, status=HTTPStatus.OK)

                    else:
                            message = 'method not alloed!'
                            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        
@api_view(['POST'])
def city_on_declined(request):
        try:
            if request.method == 'POST':
                print(request.data)
                element = xmltodict.parse(request.data['xmlmsg'])
                tans_data = json.loads(json.dumps(element)) 
                print(json.dumps(element))
                return JsonResponse({'status': True, 'message': 'Your payment has been declined.', 'data': tans_data}, status=HTTPStatus.OK)
        except Exception as e:
            message = "Something went wrong."
            return JsonResponse({'status': True, 'message': message}, status=HTTPStatus.EXPECTATION_FAILED)
        
@api_view(['POST'])
def city_on_approved(request):
        try:
            if request.method == 'POST':
                element = xmltodict.parse(request.data['xmlmsg'])
                tans_data = json.dumps(element)
                return JsonResponse({'status': True, 'message': 'Thanks for payment,You payment has been approved.', 'data': tans_data}, status=HTTPStatus.OK)
        except Exception as e:
            message = "Something went wrong."
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

@api_view(['POST'])
def city_on_cancelled(request):
        try:
            if request.method == 'POST':
                element = xmltodict.parse(request.data['xmlmsg'])
                tans_data = json.dumps(element)
                return JsonResponse({'status': True, 'message': 'Your payment has been cancelled.', 'data': tans_data}, status=HTTPStatus.OK)
        except Exception as e:
            message = "Something went wrong."
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        
@api_view(['POST'])
def bkash_post_payment(request):
        try:
            if request.user.is_authenticated:
                json_data = json.dumps(request.data)
                body_data = json.loads(json_data)
                
                user_id = body_data['user_id']
                pay_to = User.objects.get(id=user_id)
                
                print(request.user)
                
                postPayment = PostPayment()
                postPayment.payment_by = request.user
                postPayment.payment_to = pay_to
                postPayment.payment_id =  body_data['paymentID']
                postPayment.trx_id = body_data['trxID']
                postPayment.amount = body_data['amount']
                postPayment.currency = body_data['currency']
                postPayment.payment_type = body_data['payment_type']
                postPayment.merchant_invoice = body_data['merchantInvoiceNumber']
                postPayment.transaction_status = body_data['transactionStatus']
                postPayment.save()
                
                message = "Payment successfully added."
                
                return JsonResponse({'status': True, 'message' : message,  'data': json.loads(json_data)}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

@api_view(['GET'])
def payment_statement(request):
        try:
            if request.user.is_authenticated:
                payment_list = PostPayment.objects.filter(payment_to = request.user)
                
                results = []
                paginator = Paginator(payment_list, 10)
                page = request.GET.get('page', 1)
                try:
                    payment_list = paginator.page(page)
                except PageNotAnInteger:
                    payment_list = paginator.page(1)
                except EmptyPage:
                    payment_list = paginator.page(paginator.num_pages)

                user_payment_filter = PaymentSerializer(payment_list, many=True).data
                results.append(user_payment_filter)
                message = "Payment statement fetch successfully."

                return paginator_service.response_paginated(payment_list, user_payment_filter, request)
        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        
        
        
@api_view(['POST'])
def  bkash_create_payment(request):
        try:
            if request.user.is_authenticated:
                    if request.method == 'POST':
                
                        url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant'
                        data = {
                            'app_key': '5tunt4masn6pv2hnvte1sb5n3j', 
                            'app_secret': '1vggbqd4hqk9g96o9rrrp2jftvek578v7d2bnerim12a87dbrrka'
                            }
                        headers = {
                            'Content-type': 'application/json', 
                            'Accept': 'application/json',
                            'username': 'sandboxTestUser',
                            'password': 'hWD@8vtzw0'
                            }
                        r_token = requests.post(url, data=json.dumps(data), headers=headers)

                        response_data_token = json.loads(r_token.text)
                        id_token_str = str(response_data_token['id_token'])
                        id_token = response_data_token['id_token']

                        #print(response_data_token)



                        url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create'
                        data_checkout = {
                            'mode': '0011',
                            'payerReference' : '01712546965',
                            'callbackURL' : 'www.google.com',
                            'amount': "2",
                            'currency': "BDT",
                            'intent': "sale",
                            'merchantInvoiceNumber': str(uuid.uuid4()),

                            }

                        headers_checkout= {
                            "Content-Type": "application/json", 
                            "Accept": "application/json",
                            "authorization": id_token,
                            "x-app-key": "5tunt4masn6pv2hnvte1sb5n3j"
                            }

                        r_checkout = requests.post(url, data=json.dumps(data_checkout), headers=headers_checkout)

                        #print(headers_checkout)

                        response_data_checkout = json.loads(r_checkout.text)
                        #print(response_data_checkout)
                        paymentID = response_data_checkout['paymentID']
                        

                        return JsonResponse(response_data_checkout, status=HTTPStatus.OK)

                    else:
                            message = 'method not alloed!'
                            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

@api_view(['POST'])
def  bkash_execution_payments(request):
        try:
            if request.user.is_authenticated:
                    if request.method == 'POST':
                        
                        print("TEST")
                        url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant'
                        data = {
                            'app_key': '5tunt4masn6pv2hnvte1sb5n3j', 
                            'app_secret': '1vggbqd4hqk9g96o9rrrp2jftvek578v7d2bnerim12a87dbrrka'
                            }
                        headers = {
                            'Content-type': 'application/json', 
                            'Accept': 'application/json',
                            'username': 'sandboxTestUser',
                            'password': 'hWD@8vtzw0'
                            }
                        r_token = requests.post(url, data=json.dumps(data), headers=headers)

                        response_data_token = json.loads(r_token.text)
                        id_token_str = str(response_data_token['id_token'])
                        id_token = response_data_token['id_token']
                        
                        # json_data = json.loads(request.body)
                        
                        # paymentID = json_data['paymentID']
                        paymentID = str(request.POST['paymentID'])
                
                        url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/execute/' + paymentID

                        #print(url)
                        #print(id_token)

                        headers = {
                            'Accept': 'application/json',
                            'authorization': id_token,
                            'x-app-key': '5tunt4masn6pv2hnvte1sb5n3j'
                            }

                        data = {
                            "paymentID": paymentID
                            }

                        response_data = requests.post(url, data=json.dumps(data), headers=headers)
                        print(response_data)

                        r_data = json.loads(response_data.text)
                        return JsonResponse(r_data, status=HTTPStatus.OK)
                    
                    
                    else:
                            message = 'method not alloed!'
                            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)

        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
                    

