from django.http import JsonResponse


def response_paginated(page_obj, data, request):
    next_page = None
    previous_page = None
    if page_obj.has_previous():
        previous_page = request.path + "?page=" + str(page_obj.previous_page_number())
    if page_obj.has_next():
        next_page = request.path + "?page=" + str(page_obj.next_page_number())
    d = {
        'next': next_page,
        'previous': previous_page,
        'count': page_obj.paginator.count,
        'results': data
    }
    return JsonResponse({'status': True, 'data': d})
