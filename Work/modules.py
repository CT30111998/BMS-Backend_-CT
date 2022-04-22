from BMSystem.base_function import \
    create_response as my_response, \
    get_session as my_session_get, \
    get_name_from_master_user as my_name_create, \
    get_payload_error_alert as my_payload_error, \
    get_date_from_tabl_object as my_table_data_get
from BMSystem import constant
from json import loads
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster as MasterUser
from .models import AttendanceMaster as AttendMaster, CategoryMaser as CatMaster
import datetime


def get_all_user_attendance(request=None):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = my_session_get(request, constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    attend_filter = {}
    order_by = f"-{constant.WORK_MODEL_FIELDS['date']}"
    if request.body:
        get_json_response = loads(request.body)
        if constant.USER_MODEL_FIELDS['get_user_id'] in get_json_response:
            attend_filter[constant.USER_MODEL_FIELDS['user']] = \
                get_json_response[constant.USER_MODEL_FIELDS['get_user_id']]

        if constant.WORK_MODEL_FIELDS['year'] in get_json_response:
            attend_filter[constant.WORK_MODEL_FIELDS['year']] = get_json_response[
                constant.WORK_MODEL_FIELDS['year']
            ]
            if constant.WORK_MODEL_FIELDS['month'] in get_json_response:
                attend_filter[constant.WORK_MODEL_FIELDS['month']] = get_json_response[
                    constant.WORK_MODEL_FIELDS['month']
                ]
                if constant.WORK_MODEL_FIELDS['day'] in get_json_response:
                    attend_filter[constant.WORK_MODEL_FIELDS['day']] = get_json_response[
                        constant.WORK_MODEL_FIELDS['day']
                    ]

        if (constant.WORK_MODEL_FIELDS['month'] in get_json_response and
            constant.WORK_MODEL_FIELDS['year'] not in get_json_response)\
                or (constant.WORK_MODEL_FIELDS['day'] in get_json_response and
                    constant.WORK_MODEL_FIELDS['month'] not in get_json_response):
            alert = my_payload_error(constant.WORK_MODEL_FIELDS['year'], constant.WORK_MODEL_FIELDS['month'])
            return my_response(result=False, alert=alert)

        if constant.WORK_MODEL_FIELDS['date'] in get_json_response:
            attend_filter[constant.WORK_MODEL_FIELDS['date']] = get_json_response[
                constant.WORK_MODEL_FIELDS['date']
            ]

        if constant.COMMON_MODEL_FIELDS['order_by'] in get_json_response:
            if get_json_response[constant.COMMON_MODEL_FIELDS['order_by']] == constant.ORDER_BY_DATE_ASCENDING:
                order_by = constant.WORK_MODEL_FIELDS['date']

    get_all_attendance = AttendMaster.objects.all().filter(**attend_filter).order_by(order_by)
    attends_data_list = []
    for attend in get_all_attendance:
        attend_params = {
            "attend_id": getattr(attend, constant.WORK_MODEL_FIELDS['attendance_id']),
            "attend_of_user": {},
            "punch_in": getattr(attend, constant.WORK_MODEL_FIELDS['punch_in']),
            "punch_out": getattr(attend, constant.WORK_MODEL_FIELDS['punch_out']),
            "date": my_table_data_get(attend),
        }

        get_attend_user = MasterUser.objects.get(**{
            constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.USER_MODEL_FIELDS['user'])
        })
        attend_user_name = my_name_create(get_attend_user)
        attend_user_id = getattr(get_attend_user, constant.USER_MODEL_FIELDS['id'])

        attend_params['attend_of_user'].update({
            "name": attend_user_name,
            "id": attend_user_id
        })

        get_created_user = MasterUser.objects.get(**{
            constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.WORK_MODEL_FIELDS['created_by'])
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, constant.USER_MODEL_FIELDS['id'])
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, constant.WORK_MODEL_FIELDS['updated_by']):
            if getattr(attend, constant.WORK_MODEL_FIELDS['created_by']) == \
                    getattr(attend, constant.WORK_MODEL_FIELDS['updated_by']):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.WORK_MODEL_FIELDS['updated_by'])
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, constant.USER_MODEL_FIELDS['id']),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)

    if not get_all_attendance:
        return my_response(result=False, alert=constant.ATTEND_NOT_FOUND)

    return my_response(result=True, alert=constant.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def get_user_attendance(request=None):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)

    user_id = my_session_get(request, constant.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    get_attends = AttendMaster.objects.filter(**{
        constant.USER_MODEL_FIELDS['user']: user_id,
        constant.WORK_MODEL_FIELDS['month']: datetime.datetime.now().date().month,
        constant.WORK_MODEL_FIELDS['year']: datetime.datetime.now().date().year,
    })
    if not get_attends:
        return my_response(result=False, alert=constant.ATTEND_NOT_FOUND)

    attends_data_list = []
    for attend in get_attends:
        attend_params = {
            "attend_id": getattr(attend, constant.WORK_MODEL_FIELDS['attendance_id']),
            "date": my_table_data_get(attend),
            "punch_in": getattr(attend, constant.WORK_MODEL_FIELDS['punch_in']),
            "punch_out": getattr(attend, constant.WORK_MODEL_FIELDS['punch_out']),
        }
        get_created_user = MasterUser.objects.get(**{
            constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.WORK_MODEL_FIELDS['created_by'])
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, constant.USER_MODEL_FIELDS['id'])
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, constant.WORK_MODEL_FIELDS['updated_by']):
            if getattr(attend, constant.WORK_MODEL_FIELDS['created_by']) == \
                    getattr(attend, constant.WORK_MODEL_FIELDS['updated_by']):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.WORK_MODEL_FIELDS['updated_by'])
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, constant.USER_MODEL_FIELDS['id']),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)
    return my_response(result=True, alert=constant.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def create_user_attendance(request=None):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)

    get_json_data = loads(request.body)
    if constant.WORK_MODEL_FIELDS['punch_status'] not in get_json_data:
        alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.WORK_MODEL_FIELDS['punch_status']}" + \
            f" in {constant.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)

    user_id = my_session_get(request, constant.SESSION_USER_ID)
    if not user_id:
        return my_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    get_current_user = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: user_id})

    if constant.WORK_MODEL_FIELDS["emp_id"] in get_json_data:
        emp_id = get_json_data[constant.WORK_MODEL_FIELDS["emp_id"]]
        try:
            get_emp = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: emp_id})
        except:
            return my_response(result=False, alert=constant.EMP_NOT_EXIST)
    else:
        get_emp = get_current_user

    attend_params = {constant.USER_MODEL_FIELDS['user']: get_emp}

    if get_json_data[constant.WORK_MODEL_FIELDS['punch_status']] == constant.PUNCH_IN_STATUS:
        attend_params[constant.WORK_MODEL_FIELDS['punch_in']] = datetime.datetime.now().time()
    else:
        attend_params[constant.WORK_MODEL_FIELDS['punch_out']] = datetime.datetime.now().time()

    if constant.WORK_MODEL_FIELDS['attend_id'] not in get_json_data:
        attend_params[constant.WORK_MODEL_FIELDS['day']] = datetime.datetime.now().date().day
        attend_params[constant.WORK_MODEL_FIELDS['month']] = datetime.datetime.now().date().month
        attend_params[constant.WORK_MODEL_FIELDS['year']] = datetime.datetime.now().date().year
        attend_params[constant.WORK_MODEL_FIELDS['created_by']] = get_current_user
        create_attend = AttendMaster(**attend_params)
        create_attend.save()
        alert = constant.CREATE_ATTENDANCE_SUCCESSFUL
    else:
        get_attend = AttendMaster.objects.filter(**{
            constant.WORK_MODEL_FIELDS['attendance_id']: get_json_data[constant.WORK_MODEL_FIELDS['attend_id']]
        })
        if not get_attend:
            return my_response(result=False, alert=constant.ATTEND_NOT_FOUND)
        attend_params[constant.WORK_MODEL_FIELDS['updated_by']] = get_current_user
        get_attend.update(**attend_params)
        alert = constant.UPDATE_ATTENDANCE_SUCCESSFUL

    return my_response(result=True, alert=alert)


def update_user_attendance(request=None):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)
    return my_response(result=True, alert=constant.UPDATE_ATTENDANCE_SUCCESSFUL)


def delete_user_attendance(request=None):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = my_session_get(request, constant.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    get_json_data = loads(request.body)

    if constant.WORK_MODEL_FIELDS['attend_id'] not in get_json_data:
        alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.WORK_MODEL_FIELDS['attend_id']}" + \
            f" in {constant.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)
    try:
        get_attend = AttendMaster.objects.get(**{
            constant.WORK_MODEL_FIELDS['attendance_id']: get_json_data[constant.WORK_MODEL_FIELDS['attend_id']]
        })
    except:
        return my_response(result=False, alert=constant.ATTEND_NOT_FOUND)

    get_attend.delete()
    return my_response(result=True, alert=constant.DELETE_ATTENDANCE_SUCCESSFUL)


def create_category(request):
    if not request:
        return my_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = my_session_get(request, constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    try:
        get_json_response = loads(request.body)
        get_cat_name = get_json_response[constant.WORK_MODEL_FIELDS['cat_name']]
        user_id = get_json_response[constant.USER_MODEL_FIELDS['get_user_id']]
    except:
        alert = my_payload_error(
            constant.WORK_MODEL_FIELDS['cat_name'],
            constant.USER_MODEL_FIELDS['get_user_id']
        )
        return my_response(result=False, alert=alert)

    get_user_master = AuthUser.objects.get(
        **{constant.USER_MODEL_FIELDS['id']: user_id}
    )
    create_cat = CatMaster(**{
        constant.WORK_MODEL_FIELDS['cat_name']: get_cat_name,
        constant.WORK_MODEL_FIELDS['created_by']: get_user_master
    })
    create_cat.save()
    return my_response(result=True, alert=constant.CATEGORY_CREATE_SUCCESSFUL)
