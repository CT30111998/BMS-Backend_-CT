from rest_framework.response import Response
from django.http import JsonResponse
import re


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return JsonResponse(get)


def create_session(request, key, value):
    try:
        request.session[key] = value
        return value
    except:
        return None


def get_session(request, key):
    try:
        value = request.session[key]
        return value
    except:
        return None


def del_session(request, key):
    try:
        del request.session[key]
        return 1
    except:
        return None


def null_valid(fields):
    not_null = True
    for li in fields:
        if li == "" or li is None:
            not_null = False
            break
    return not_null


def pass_valid(password):
    check = str(password)
    if len(check) >= 8:
        return True
    else:
        return False


def email_valid(email):
    regex = r"^[a-z0-9]+[\._-]*[a-z0-9]*[@][a-z0-9]+[.][a-z]{1,3}[.]?[a-z]{0,2}$"

    if re.fullmatch(regex, email):
        return True
    else:
        return False
