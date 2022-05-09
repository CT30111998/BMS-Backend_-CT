from BMSystem import model_fields, constants
from base.query_modules import get_data
from Auth.models import AuthToken
import re
from Auth.jwt_module import get_token_from_request


def save_file_storage(request):
    file = request.FILES['uploadedFile']
    # file_name = default_storage.save(file.name, file)
    # return JsonResponse(file_name, safe=False)


def get_name_from_master_user(user_objects):
    user_name = f"{getattr(user_objects, model_fields.FIRST_NAME)} " + \
        f"{getattr(user_objects, model_fields.LAST_NAME)}"
    return user_name


def get_date_from_tabl_object(table_object):
    date = f"{getattr(table_object, model_fields.YEAR)}-" +\
            f"{getattr(table_object, model_fields.MONTH)}-" +\
            f"{getattr(table_object, model_fields.DAY)}"

    return date


def get_user_id_from_request(request, method=constants.GET):
    token = get_token_from_request(request)
    user_object = get_data(model=AuthToken, filters={'token': token}).first().user_master
    user_id = user_object.id
    if not user_id:
        try:
            if 'user_id' in request.data:
                user_id = request.data['user_id']
            else:
                user_id = request.GET['user_id']
        except:
            return None
    return user_id


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
    alert = f"{constants.PAYLOAD_DATA_ERROR} {field_name} in {constants.PAYLOAD_DATA_FORMAT}"
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
