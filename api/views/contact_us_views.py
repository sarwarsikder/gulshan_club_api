
from http import HTTPStatus
from rest_framework.decorators import action, permission_classes, api_view, authentication_classes
from django.http import JsonResponse
from api.models import ContactUs


@api_view(['POST'])
def  contact_request(request):
        try:
            if request.user.is_authenticated:
                    if request.method == 'POST':
                        contactUs = ContactUs()
                        contactUs.created_by = request.user
                        contactUs.name = request.POST['name']
                        contactUs.account_number = request.POST['account_number']
                        contactUs.message = request.POST['message']
                        contactUs.save()
                        
                        message = "Request has been sent."
                        return JsonResponse({'status': True, 'message': message}, status=HTTPStatus.OK)
            else:
                message = "Please valid User."
                return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
        except Exception as e:
            message = "Something went wrong." + str(e)
            print(str(e))
            return JsonResponse({'status': True, 'data': message}, status=HTTPStatus.EXPECTATION_FAILED)
