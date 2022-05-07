from BMSystem.base_function import \
    create_response as my_response, \
    get_session as my_session_get, \
    get_name_from_master_user as my_name_create, \
    get_payload_error_alert as my_payload_error, \
    get_date_from_tabl_object as my_date_get_from_table
from BMSystem import constants
from json import loads
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster as MasterUser
from .models import AttendanceMaster as AttendMaster, CategoryMaser as CatMaster, FeedbackMaster
import datetime
from base.query_modules import save_data, get_data, update_data_by_fields, update_data_by_filters
from datetime import datetime


def get_all_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    attend_filter = {}
    order_by = f"-{constants.WORK_MODEL_FIELDS['date']}"
    if request.body:
        get_json_response = loads(request.body)
        if constants.USER_MODEL_FIELDS['get_user_id'] in get_json_response:
            attend_filter[constants.USER_MODEL_FIELDS['user']] = \
                get_json_response[constants.USER_MODEL_FIELDS['get_user_id']]

        if constants.WORK_MODEL_FIELDS['year'] in get_json_response:
            attend_filter[constants.WORK_MODEL_FIELDS['year']] = get_json_response[
                constants.WORK_MODEL_FIELDS['year']
            ]
            if constants.WORK_MODEL_FIELDS['month'] in get_json_response:
                attend_filter[constants.WORK_MODEL_FIELDS['month']] = get_json_response[
                    constants.WORK_MODEL_FIELDS['month']
                ]
                if constants.WORK_MODEL_FIELDS['day'] in get_json_response:
                    attend_filter[constants.WORK_MODEL_FIELDS['day']] = get_json_response[
                        constants.WORK_MODEL_FIELDS['day']
                    ]

        if (constants.WORK_MODEL_FIELDS['month'] in get_json_response and
            constants.WORK_MODEL_FIELDS['year'] not in get_json_response) \
                or (constants.WORK_MODEL_FIELDS['day'] in get_json_response and
                    constants.WORK_MODEL_FIELDS['month'] not in get_json_response):
            alert = my_payload_error(constants.WORK_MODEL_FIELDS['year'], constants.WORK_MODEL_FIELDS['month'])
            return my_response(result=False, alert=alert)

        if constants.WORK_MODEL_FIELDS['date'] in get_json_response:
            attend_filter[constants.WORK_MODEL_FIELDS['date']] = get_json_response[
                constants.WORK_MODEL_FIELDS['date']
            ]

        if constants.COMMON_MODEL_FIELDS['order_by'] in get_json_response:
            if get_json_response[constants.COMMON_MODEL_FIELDS['order_by']] == constants.ORDER_BY_DATE_ASCENDING:
                order_by = constants.WORK_MODEL_FIELDS['date']

    get_all_attendance = AttendMaster.objects.all().filter(**attend_filter).order_by(order_by)
    attends_data_list = []
    for attend in get_all_attendance:
        attend_params = {
            "attend_id": getattr(attend, constants.WORK_MODEL_FIELDS['attendance_id']),
            "attend_of_user": {},
            "punch_in": getattr(attend, constants.WORK_MODEL_FIELDS['punch_in']),
            "punch_out": getattr(attend, constants.WORK_MODEL_FIELDS['punch_out']),
            "date": my_date_get_from_table(attend),
        }

        get_attend_user = MasterUser.objects.get(**{
            constants.USER_MODEL_FIELDS['user']: getattr(attend, constants.USER_MODEL_FIELDS['user'])
        })
        attend_user_name = my_name_create(get_attend_user)
        attend_user_id = getattr(get_attend_user, constants.USER_MODEL_FIELDS['id'])

        attend_params['attend_of_user'].update({
            "name": attend_user_name,
            "id": attend_user_id
        })

        get_created_user = MasterUser.objects.get(**{
            constants.USER_MODEL_FIELDS['user']: getattr(attend, constants.WORK_MODEL_FIELDS['created_by'])
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, constants.USER_MODEL_FIELDS['id'])
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, constants.WORK_MODEL_FIELDS['updated_by']):
            if getattr(attend, constants.WORK_MODEL_FIELDS['created_by']) == \
                    getattr(attend, constants.WORK_MODEL_FIELDS['updated_by']):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    constants.USER_MODEL_FIELDS['user']: getattr(attend, constants.WORK_MODEL_FIELDS['updated_by'])
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, constants.USER_MODEL_FIELDS['id']),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)

    if not get_all_attendance:
        return my_response(result=False, alert=constants.ATTEND_NOT_FOUND)

    return my_response(result=True, alert=constants.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def get_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=constants.UNEXPECTED_ERROR)

    # user_id = my_session_get(request, constants.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)

    get_attends = AttendMaster.objects.filter(**{
        constants.USER_MODEL_FIELDS['user']: user_id,
        constants.WORK_MODEL_FIELDS['month']: datetime.datetime.now().date().month,
        constants.WORK_MODEL_FIELDS['year']: datetime.datetime.now().date().year,
    })
    if not get_attends:
        return my_response(result=False, alert=constants.ATTEND_NOT_FOUND)

    attends_data_list = []
    for attend in get_attends:
        attend_params = {
            "attend_id": getattr(attend, constants.WORK_MODEL_FIELDS['attendance_id']),
            "date": my_date_get_from_table(attend),
            "punch_in": getattr(attend, constants.WORK_MODEL_FIELDS['punch_in']),
            "punch_out": getattr(attend, constants.WORK_MODEL_FIELDS['punch_out']),
        }
        get_created_user = MasterUser.objects.get(**{
            constants.USER_MODEL_FIELDS['user']: getattr(attend, constants.WORK_MODEL_FIELDS['created_by'])
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, constants.USER_MODEL_FIELDS['id'])
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, constants.WORK_MODEL_FIELDS['updated_by']):
            if getattr(attend, constants.WORK_MODEL_FIELDS['created_by']) == \
                    getattr(attend, constants.WORK_MODEL_FIELDS['updated_by']):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    constants.USER_MODEL_FIELDS['user']: getattr(attend, constants.WORK_MODEL_FIELDS['updated_by'])
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, constants.USER_MODEL_FIELDS['id']),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)
    return my_response(result=True, alert=constants.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def create_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=constants.UNEXPECTED_ERROR)

    get_json_data = request.data
    if constants.WORK_MODEL_FIELDS['punch_status'] not in get_json_data:
        alert = f"{constants.PAYLOAD_DATA_ERROR} {constants.WORK_MODEL_FIELDS['punch_status']}" + \
                f" in {constants.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)

    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)

    get_current_user = AuthUser.objects.get(**{constants.USER_MODEL_FIELDS['id']: user_id})

    if constants.WORK_MODEL_FIELDS["emp_id"] in get_json_data:
        emp_id = get_json_data[constants.WORK_MODEL_FIELDS["emp_id"]]
        try:
            get_emp = AuthUser.objects.get(**{constants.USER_MODEL_FIELDS['id']: emp_id})
        except:
            return my_response(result=False, alert=constants.EMP_NOT_EXIST)
    else:
        get_emp = get_current_user

    attend_params = {constants.USER_MODEL_FIELDS['user']: get_emp}
    if get_json_data[constants.WORK_MODEL_FIELDS['punch_status']] == constants.PUNCH_IN_STATUS:
        attend_params[constants.WORK_MODEL_FIELDS['punch_in']] = datetime.datetime.now().time()
    else:
        attend_params[constants.WORK_MODEL_FIELDS['punch_out']] = datetime.datetime.now().time()

    if constants.WORK_MODEL_FIELDS['attend_id'] not in get_json_data:
        attend_params[constants.WORK_MODEL_FIELDS['day']] = datetime.datetime.now().date().day
        attend_params[constants.WORK_MODEL_FIELDS['month']] = datetime.datetime.now().date().month
        attend_params[constants.WORK_MODEL_FIELDS['year']] = datetime.datetime.now().date().year
        attend_params[constants.WORK_MODEL_FIELDS['created_by']] = get_current_user
        create_attend = AttendMaster(**attend_params)
        create_attend.save()
        alert = constants.CREATE_ATTENDANCE_SUCCESSFUL
    else:
        get_attend = AttendMaster.objects.filter(**{
            constants.WORK_MODEL_FIELDS['attendance_id']: get_json_data[constants.WORK_MODEL_FIELDS['attend_id']]
        })
        if not get_attend:
            return my_response(result=False, alert=constants.ATTEND_NOT_FOUND)
        attend_params[constants.WORK_MODEL_FIELDS['updated_by']] = get_current_user
        get_attend.update(**attend_params)
        alert = constants.UPDATE_ATTENDANCE_SUCCESSFUL

    return my_response(result=True, alert=alert)


# def update_user_attendance(request=None):
#     if not request:
#         return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
#     return my_response(result=True, alert=constants.UPDATE_ATTENDANCE_SUCCESSFUL)


def delete_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    get_json_data = loads(request.body)

    if constants.WORK_MODEL_FIELDS['attend_id'] not in get_json_data:
        alert = f"{constants.PAYLOAD_DATA_ERROR} {constants.WORK_MODEL_FIELDS['attend_id']}" + \
                f" in {constants.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)
    try:
        get_attend = AttendMaster.objects.get(**{
            constants.WORK_MODEL_FIELDS['attendance_id']: get_json_data[constants.WORK_MODEL_FIELDS['attend_id']]
        })
    except:
        return my_response(result=False, alert=constants.ATTEND_NOT_FOUND)

    get_attend.delete()
    return my_response(result=True, alert=constants.DELETE_ATTENDANCE_SUCCESSFUL)


def get_all_cat(request, user_id=None):
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     user_id = loads(request.body)[constants.USER_MODEL_FIELDS['get_user_id']]
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    get_cats = CatMaster.objects.all()
    cat_list = []
    for cat in get_cats:
        get_user = MasterUser.objects.get(**{constants.USER_MODEL_FIELDS['user']: user_id})
        user_name = my_name_create(get_user)
        cat_dict = {
            constants.WORK_MODEL_FIELDS["cat_name"]: getattr(cat, constants.WORK_MODEL_FIELDS['cat_name']),
            constants.WORK_MODEL_FIELDS["created_by"]: {
                "id": user_id, "name": user_name
            }
        }
        cat_list.append(cat_dict)
    return my_response(result=True, alert=constants.DATA_FETCH_SUCCESSFUL, data=cat_list)


def create_category(request, user_id=None):
    if not request:
        return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
    try:
        get_json_response = loads(request.body)
        get_cat_name = get_json_response[constants.WORK_MODEL_FIELDS['cat_name']].capitalize()
        cat_id = None
        if constants.WORK_MODEL_FIELDS['get_cat_id'] in get_json_response:
            cat_id = get_json_response['get_cat_id']

    except:
        alert = my_payload_error(
            constants.WORK_MODEL_FIELDS['cat_name'],
        )
        return my_response(result=False, alert=alert)
    get_user_master = AuthUser.objects.get(
        **{constants.USER_MODEL_FIELDS['id']: user_id}
    )
    cat_params = {
        constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name,
        constants.WORK_MODEL_FIELDS['created_by']: get_user_master
    }
    if cat_id:
        get_cat = CatMaster.objects.filter(**{
            constants.WORK_MODEL_FIELDS['cat_id']: cat_id
        })
        if not get_cat:
            alert = constants.CAT_NOT_EXIST
        else:
            get_cat.update(**cat_params)
            alert = constants.CAT_UPDATE_SUCCESSFUL
    else:
        try:
            get_cat = CatMaster.objects.get(**{
                constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name
            })
            alert = constants.CAT_ALREADY_EXIST
        except:
            create_cat = CatMaster(**cat_params)
            create_cat.save()
            alert = constants.CATEGORY_CREATE_SUCCESSFUL
    return my_response(result=True, alert=alert)


def get_feedback(request):
    request_data = request.GET
    feedback_object = get_data(
        model=FeedbackMaster,
        filters={'id': request_data['feedback_id']} if 'feedback_id' in request_data else None
    )
    if not feedback_object:
        return my_response(alert=constants.FEEDBACK_NOT_EXIST)
    data_list = list()
    for feedback in feedback_object:
        feedback_dict = {
            'id': feedback.id,
            'feedback': feedback.feedback,
            'created_by': feedback.created_by.id,
        }
        data_list.append(feedback_dict)
    return my_response(result=True, alert=constants.FEEDBACK_GET_SUCCESS, data=data_list)


def create_feedback(request, user_id=None):
    request_data = request.data
    user_object = get_data(model=AuthUser, filters={'id': user_id})
    if not user_object:
        return my_response(alert=constants.USER_NOT_EXIST)

    feedback_save = save_data(model=FeedbackMaster, fields={
        constants.WORK_MODEL_FIELDS['created_by']: user_object.first(),
        'feedback': request_data['feedback'].capitalize(),
        'created_time': datetime.now()
    })

    if not feedback_save:
        return my_response(alert=constants.UNEXPECTED_ERROR)

    return my_response(result=True, alert=constants.FEEDBACK_CREATE_SUCCESS)


def update_feedback(request):
    request_data = request.data
    feedback_id = request_data['feedback_id']
    feedback = request_data['feedback'].capitalize()

    feedback_object = update_data_by_filters(
        model=FeedbackMaster,
        filters={'id': feedback_id},
        fields={'feedback': feedback}
    )
    if not feedback_object:
        return my_response(alert=constants.UNEXPECTED_ERROR)

    return my_response(result=True, alert=constants.FEEDBACK_UPDATE_SUCCESS)


def delete_feedback(request, user_id=None):
    request_data = request.GET
    feedback_id = request_data['feedback_id']
    feedback_object = get_data(model=FeedbackMaster, filters={'id': feedback_id})
    if not feedback_object:
        return my_response(alert=constants.FEEDBACK_NOT_EXIST)

    feedback_object.delete()
    return my_response(result=True, alert=constants.FEEDBACK_DELETE_SUCCESS)