from rest_framework.response import Response
from json import dumps, loads
from django.http import JsonResponse


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return JsonResponse(get)
