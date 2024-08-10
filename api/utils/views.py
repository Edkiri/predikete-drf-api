from django.http import JsonResponse


def custom_page_not_found_view(request, exception):
    return JsonResponse({'error': 'The requested resource was not found'}, status=404)


def custom_server_error_view(request):
    return JsonResponse({'error': 'A server error occurred'}, status=500)


def custom_permission_denied_view(request, exception):
    return JsonResponse({'error': 'Permission denied'}, status=403)


def custom_bad_request_view(request, exception):
    return JsonResponse({'error': 'Bad request'}, status=400)
