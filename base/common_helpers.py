from rest_framework.response import Response
from pagecalc import Paginator
from datetime import datetime
from base.query_modules import get_data
from Auth.models import AuthToken
import re
from Auth.jwt_module import get_token_from_request
from BMSystem import constants, decimal_constants, response_messages, model_fields


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return Response(get)


def convert_time_to_timestamp(time=None):
    if not time:
        time = datetime.now()
    return int(datetime.timestamp(time))


# email validation functions
def check_email_format(email):
    regex = r"^[a-z0-9]+[\._-]*[a-z0-9]*[@][a-z0-9]+[.][a-z]{1,3}[.]?[a-z]{0,2}$"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def get_sort_key(sort_field=None, sort_id=None):
    if sort_id:
        sort_id = int(sort_id)
    return '-' + sort_field if sort_id == decimal_constants.DESCENDING_ORDER else sort_field


def get_search_params(
        query_params=None, search_query_param='filters', search_field=None, search_value=None
):
    if search_value:
        query_param = {'{}__icontains'.format(search_field): search_value}
        query_params[search_query_param].update(query_param)


def paginate_records(page=None, record_list=None, records_per_page=decimal_constants.PAGE_SIZE, list_name=None):
    page = page - 1
    paginator = Paginator(total=len(record_list), by=records_per_page)
    page_details = paginator.paginate(page + 1)

    starting_record = page * records_per_page
    end_record = page * records_per_page + records_per_page
    required_record_list = record_list[starting_record: end_record]

    required_page_details = {
        'page': {
            'page': page_details['page']['current'],
            'pageSize': records_per_page,
            'totalEntrys': page_details['item']['totalCount'],
            'totalpage': page_details['page']['count'],
            'start': starting_record + 1,
            'end': starting_record + len(required_record_list)
        },
        list_name: required_record_list
    }
    return required_page_details


def save_file_storage(request):
    file = request.FILES['uploadedFile']
    # file_name = default_storage.save(file.name, file)
    # return JsonResponse(file_name, safe=False)


def get_name_from_master_user(user_objects):
    user_name = f"{getattr(user_objects, model_fields.FIRST_NAME)} " + \
        f"{getattr(user_objects, model_fields.LAST_NAME)}"
    return user_name


def get_payload_error_alert(*fields):
    field_name = []
    for field in fields:
        field_name.append(str(field))
    alert = f"{response_messages.PAYLOAD_DATA_ERROR} {field_name} in {response_messages.PAYLOAD_DATA_FORMAT}"
    return alert


def get_date_from_tabl_object(table_object):
    date = f"{getattr(table_object, model_fields.YEAR)}-" +\
            f"{getattr(table_object, model_fields.MONTH)}-" +\
            f"{getattr(table_object, model_fields.DAY)}"

    return date


def get_user_id_from_request(request, method=constants.GET):
    token = get_token_from_request(request)
    if not token:
        return None
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