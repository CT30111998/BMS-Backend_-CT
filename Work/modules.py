from BMSystem.base_function import *
from json import loads
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster as MasterUser
from .models import AttendanceMaster as AttendMaster
import datetime


def get_all_user_attendance(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request, constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    if request.body:
        get_json_response = loads(request.body)
    # get_all_attendance = AttendMaster.objetcs
    return create_response(result=True, alert=constant.DATA_FETCH_SUCCESSFUL)


def get_user_attendance(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)

    user_id = get_session(request, constant.SESSION_USER_ID)

    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    get_attends = AttendMaster.objects.filter(**{
        constant.USER_MODEL_FIELDS['user']: user_id,
        constant.WORK_MODEL_FIELDS['month']: datetime.datetime.now().date().month,
        constant.WORK_MODEL_FIELDS['year']: datetime.datetime.now().date().year,
    })
    if not get_attends:
        return create_response(result=False, alert=constant.ATTEND_NOT_FOUND)
    attends_data_list = []
    for attend in get_attends:
        attend_params = {
            "attend_id": getattr(attend, constant.WORK_MODEL_FIELDS['attendance_id']),
            "date": get_date_from_tabl_object(attend),
            "punch_in": getattr(attend, constant.WORK_MODEL_FIELDS['punch_in']),
            "punch_out": getattr(attend, constant.WORK_MODEL_FIELDS['punch_out']),
        }
        get_created_user = MasterUser.objects.get(**{
            constant.USER_MODEL_FIELDS['user']: getattr(attend, constant.WORK_MODEL_FIELDS['created_by'])
        })
        created_user_name = get_name_from_master_user(get_created_user)
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
                update_user_name = get_name_from_master_user(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, constant.USER_MODEL_FIELDS['id']),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)
    return create_response(result=True, alert=constant.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def create_user_attendance(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)

    get_json_data = loads(request.body)
    if constant.WORK_MODEL_FIELDS['punch_status'] not in get_json_data:
        alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.WORK_MODEL_FIELDS['punch_status']}" + \
            f" in {constant.PAYLOAD_DATA_FORMAT}"
        return create_response(result=False, alert=alert)

    user_id = get_session(request, constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    get_current_user = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: user_id})

    if constant.WORK_MODEL_FIELDS["emp_id"] in get_json_data:
        emp_id = get_json_data[constant.WORK_MODEL_FIELDS["emp_id"]]
        try:
            get_emp = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: emp_id})
        except:
            return create_response(result=False, alert=constant.EMP_NOT_EXIST)
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
            return create_response(result=False, alert=constant.ATTEND_NOT_FOUND)
        attend_params[constant.WORK_MODEL_FIELDS['updated_by']] = get_current_user
        get_attend.update(**attend_params)
        alert = constant.UPDATE_ATTENDANCE_SUCCESSFUL

    return create_response(result=True, alert=alert)


def update_user_attendance(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    return create_response(result=True, alert=constant.UPDATE_ATTENDANCE_SUCCESSFUL)


def delete_user_attendance(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request, constant.SESSION_USER_ID)

    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    get_json_data = loads(request.body)

    if constant.WORK_MODEL_FIELDS['attend_id'] not in get_json_data:
        alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.WORK_MODEL_FIELDS['attend_id']}" + \
            f" in {constant.PAYLOAD_DATA_FORMAT}"
        return create_response(result=False, alert=alert)
    try:
        get_attend = AttendMaster.objects.get(**{
            constant.WORK_MODEL_FIELDS['attendance_id']: get_json_data[constant.WORK_MODEL_FIELDS['attend_id']]
        })
    except:
        return create_response(result=False, alert=constant.ATTEND_NOT_FOUND)

    get_attend.delete()
    return create_response(result=True, alert=constant.DELETE_ATTENDANCE_SUCCESSFUL)
