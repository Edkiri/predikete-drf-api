from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return JsonResponse({'detail': str(exc)}, status=500)

    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', str(response.data)),
                'errors': response.data
            }
        }
        return Response(custom_response_data, status=response.status_code)

    return response
