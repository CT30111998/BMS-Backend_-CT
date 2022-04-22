from rest_framework.response import Response
from django.http import JsonResponse
from . import constant
import re
from json import loads


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return JsonResponse(get)


def save_file_storage(request):
    file = request.FILES['uploadedFile']
    # file_name = default_storage.save(file.name, file)
    # return JsonResponse(file_name, safe=False)


def get_name_from_master_user(user_objects):
    user_name = f"{getattr(user_objects, constant.USER_MODEL_FIELDS['first_name'])} " + \
        f"{getattr(user_objects, constant.USER_MODEL_FIELDS['last_name'])}"
    return user_name


def get_date_from_tabl_object(table_object):
    date = f"{getattr(table_object, constant.WORK_MODEL_FIELDS['year'])}-" +\
            f"{getattr(table_object, constant.WORK_MODEL_FIELDS['month'])}-" +\
            f"{getattr(table_object, constant.WORK_MODEL_FIELDS['day'])}"
    return date


def check_user_loging(request):
    user_id = get_session(request, constant.SESSION_USER_ID)
    if not user_id:
        try:
            user_id = loads(request.body)[constant.USER_MODEL_FIELDS['get_user_id']]
        except:
            return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    return create_response(result=True, data=user_id)


def check_response_result(response=None):
    get_response = response
    try:
        print("RESPONSE: ", get_response)
    except:
        return False
    if not get_response['result']:
        return False
    return get_response['data']


def get_payload_error_alert(*fields):
    field_name = []
    for field in fields:
        field_name.append(str(field))
    alert = f"{constant.PAYLOAD_DATA_ERROR} {field_name} in {constant.PAYLOAD_DATA_FORMAT}"
    return alert


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
