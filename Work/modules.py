from BMSystem.base_function import \
    get_session as my_session_get, \
    get_name_from_master_user as my_name_create, \
    get_payload_error_alert as my_payload_error, \
    get_date_from_tabl_object as my_date_get_from_table
from BMSystem import constants, response_messages, model_fields, decimal_constants
from base.common_helpers import create_response as my_response
from json import loads
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster as MasterUser
from .models import AttendanceMaster as AttendMaster, FeedbackMaster
import datetime
from base.query_modules import save_data, get_data, update_data_by_fields, update_data_by_filters
from datetime import datetime


def get_all_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    attend_filter = {}
    order_by = f"-{model_fields.DATE}"
    if request.body:
        get_json_response = loads(request.body)
        if model_fields.USER_ID in get_json_response:
            attend_filter[model_fields.USER] = \
                get_json_response[model_fields.USER_ID]

        if model_fields.YEAR in get_json_response:
            attend_filter[model_fields.YEAR] = get_json_response[
                model_fields.YEAR
            ]
            if model_fields.MONTH in get_json_response:
                attend_filter[model_fields.MONTH] = get_json_response[
                    model_fields.MONTH
                ]
                if model_fields.DAY in get_json_response:
                    attend_filter[model_fields.DAY] = get_json_response[
                        model_fields.DAY
                    ]

        if (model_fields.MONTH in get_json_response and
            model_fields.YEAR not in get_json_response) \
                or (model_fields.DAY in get_json_response and
                    model_fields.MONTH not in get_json_response):
            alert = my_payload_error(model_fields.YEAR, model_fields.MONTH)
            return my_response(result=False, alert=alert)

        if model_fields.DATE in get_json_response:
            attend_filter[model_fields.DATE] = get_json_response[
                model_fields.DATE
            ]

        if model_fields.ORDER_BY in get_json_response:
            if get_json_response[model_fields.ORDER_BY] == decimal_constants.ORDER_BY_DATE_ASCENDING:
                order_by = model_fields.DATE

    get_all_attendance = AttendMaster.objects.all().filter(**attend_filter).order_by(order_by)
    attends_data_list = []
    for attend in get_all_attendance:
        attend_params = {
            "attend_id": getattr(attend, model_fields.ID),
            "attend_of_user": {},
            "punch_in": getattr(attend, model_fields.PUNCH_IN),
            "punch_out": getattr(attend, model_fields.PUNCH_OUT),
            "date": my_date_get_from_table(attend),
        }

        get_attend_user = MasterUser.objects.get(**{
            model_fields.USER: getattr(attend, model_fields.USER)
        })
        attend_user_name = my_name_create(get_attend_user)
        attend_user_id = getattr(get_attend_user, model_fields.ID)

        attend_params['attend_of_user'].update({
            "name": attend_user_name,
            "id": attend_user_id
        })

        get_created_user = MasterUser.objects.get(**{
            model_fields.USER: getattr(attend, model_fields.CREATED_BY)
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, model_fields.ID)
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, model_fields.UPDATED_BY):
            if getattr(attend, model_fields.CREATED_BY) == \
                    getattr(attend, model_fields.UPDATED_BY):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    model_fields.USER: getattr(attend, model_fields.UPDATED_BY)
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, model_fields.ID),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)

    if not get_all_attendance:
        return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)

    return my_response(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def get_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)

    # user_id = my_session_get(request, constants.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)

    get_attends = AttendMaster.objects.filter(**{
        model_fields.USER: user_id,
        model_fields.MONTH: datetime.datetime.now().date().month,
        model_fields.YEAR: datetime.datetime.now().date().year,
    })
    if not get_attends:
        return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)

    attends_data_list = []
    for attend in get_attends:
        attend_params = {
            "attend_id": getattr(attend, model_fields.ID),
            "date": my_date_get_from_table(attend),
            "punch_in": getattr(attend, model_fields.PUNCH_IN),
            "punch_out": getattr(attend, model_fields.PUNCH_OUT),
        }
        get_created_user = MasterUser.objects.get(**{
            model_fields.USER: getattr(attend, model_fields.CREATED_BY)
        })
        created_user_name = my_name_create(get_created_user)
        created_user_id = getattr(get_created_user, model_fields.ID)
        attend_params['created_by'] = {
            'user_id': created_user_id,
            'user_name': created_user_name
        }
        if getattr(attend, model_fields.UPDATED_BY):
            if getattr(attend, model_fields.CREATED_BY) == \
                    getattr(attend, model_fields.UPDATED_BY):
                attend_params['updated_by'] = {
                    'user_id': created_user_id,
                    'user_name': created_user_name
                }
            else:
                get_updated_user = MasterUser.objects.get(**{
                    model_fields.USER: getattr(attend, model_fields.UPDATED_BY)
                })
                update_user_name = my_name_create(get_updated_user)
                attend_params['updated_by'] = {
                    'user_id': getattr(get_updated_user, model_fields.ID),
                    'user_name': update_user_name
                }
        attends_data_list.append(attend_params)
    return my_response(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=attends_data_list)


def create_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)

    get_json_data = request.data
    if model_fields.PUNCH_IN not in get_json_data:
        alert = f"{response_messages.PAYLOAD_DATA_ERROR} {model_fields.PUNCH_IN}" + \
                f" in {response_messages.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)

    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)

    get_current_user = AuthUser.objects.get(**{model_fields.ID: user_id})

    if "emp_id" in get_json_data:
        emp_id = get_json_data["emp_id"]
        try:
            get_emp = AuthUser.objects.get(**{model_fields.ID: emp_id})
        except:
            return my_response(result=False, alert=response_messages.EMP_NOT_EXIST)
    else:
        get_emp = get_current_user

    attend_params = {model_fields.USER: get_emp}
    if get_json_data[model_fields.PUNCH_IN] == decimal_constants.PUNCH_IN_STATUS:
        attend_params[model_fields.PUNCH_IN] = datetime.datetime.now().time()
    else:
        attend_params[model_fields.PUNCH_OUT] = datetime.datetime.now().time()

    if model_fields.ATTEND_ID not in get_json_data:
        attend_params[model_fields.DAY] = datetime.datetime.now().date().day
        attend_params[model_fields.MONTH] = datetime.datetime.now().date().month
        attend_params[model_fields.YEAR] = datetime.datetime.now().date().year
        attend_params[model_fields.CREATED_BY] = get_current_user
        create_attend = AttendMaster(**attend_params)
        create_attend.save()
        alert = response_messages.CREATE_ATTENDANCE_SUCCESSFUL
    else:
        get_attend = AttendMaster.objects.filter(**{
            model_fields.ID: get_json_data[model_fields.ATTEND_ID]
        })
        if not get_attend:
            return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)
        attend_params[model_fields.UPDATED_BY] = get_current_user
        get_attend.update(**attend_params)
        alert = response_messages.UPDATE_ATTENDANCE_SUCCESSFUL

    return my_response(result=True, alert=alert)


# def update_user_attendance(request=None):
#     if not request:
#         return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
#     return my_response(result=True, alert=constants.UPDATE_ATTENDANCE_SUCCESSFUL)


def delete_user_attendance(request=None, user_id=None):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)

    # if not user_id:
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    get_json_data = loads(request.body)

    if model_fields.ATTEND_ID not in get_json_data:
        alert = f"{response_messages.PAYLOAD_DATA_ERROR} {model_fields.ATTEND_ID}" + \
                f" in {response_messages.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)
    try:
        get_attend = AttendMaster.objects.get(**{
            model_fields.ID: get_json_data[model_fields.ATTEND_ID]
        })
    except:
        return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)

    get_attend.delete()
    return my_response(result=True, alert=response_messages.DELETE_ATTENDANCE_SUCCESSFUL)


def get_all_cat(request, user_id=None):
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     user_id = loads(request.body)[model_fields.USER_ID]
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    # get_cats = CatMaster.objects.all()
    cat_list = []
    # for cat in get_cats:
    #     get_user = MasterUser.objects.get(**{model_fields.USER: user_id})
    #     user_name = my_name_create(get_user)
    #     cat_dict = {
    #         constants.WORK_MODEL_FIELDS["cat_name"]: getattr(cat, constants.WORK_MODEL_FIELDS['cat_name']),
    #         constants.WORK_MODEL_FIELDS["created_by"]: {
    #             "id": user_id, "name": user_name
    #         }
    #     }
    #     cat_list.append(cat_dict)
    return my_response(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=cat_list)


def create_category(request, user_id=None):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # try:
    #     get_json_response = loads(request.body)
    #     get_cat_name = get_json_response[constants.WORK_MODEL_FIELDS['cat_name']].capitalize()
    #     cat_id = None
    #     if constants.WORK_MODEL_FIELDS['get_cat_id'] in get_json_response:
    #         cat_id = get_json_response['get_cat_id']
    #
    # except:
    #     alert = my_payload_error(
    #         constants.WORK_MODEL_FIELDS['cat_name'],
    #     )
    #     return my_response(result=False, alert=alert)
    # get_user_master = AuthUser.objects.get(
    #     **{model_fields.ID: user_id}
    # )
    # cat_params = {
    #     constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name,
    #     model_fields.CREATED_BY: get_user_master
    # }
    # if cat_id:
    #     get_cat = CatMaster.objects.filter(**{
    #         constants.WORK_MODEL_FIELDS['cat_id']: cat_id
    #     })
    #     if not get_cat:
    #         alert = constants.CAT_NOT_EXIST
    #     else:
    #         get_cat.update(**cat_params)
    #         alert = constants.CAT_UPDATE_SUCCESSFUL
    # else:
    #     try:
    #         get_cat = CatMaster.objects.get(**{
    #             constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name
    #         })
    #         alert = constants.CAT_ALREADY_EXIST
    #     except:
    #         create_cat = CatMaster(**cat_params)
    #         create_cat.save()
    #         alert = constants.CATEGORY_CREATE_SUCCESSFUL
    return my_response(result=True)


def get_feedback(request):
    request_data = request.GET
    feedback_object = get_data(
        model=FeedbackMaster,
        filters={'id': request_data['feedback_id']} if 'feedback_id' in request_data else None
    )
    if not feedback_object:
        return my_response(alert=response_messages.FEEDBACK_NOT_EXIST)
    data_list = list()
    for feedback in feedback_object:
        feedback_dict = {
            'id': feedback.id,
            'feedback': feedback.feedback,
            'created_by': feedback.created_by.id,
        }
        data_list.append(feedback_dict)
    return my_response(result=True, alert=response_messages.FEEDBACK_GET_SUCCESS, data=data_list)


def create_feedback(request, user_id=None):
    request_data = request.data
    user_object = get_data(model=AuthUser, filters={'id': user_id})
    if not user_object:
        return my_response(alert=response_messages.USER_NOT_EXIST)

    feedback_save = save_data(model=FeedbackMaster, fields={
        model_fields.CREATED_BY: user_object.first(),
        'feedback': request_data['feedback'].capitalize(),
        'created_time': datetime.now()
    })

    if not feedback_save:
        return my_response(alert=response_messages.UNEXPECTED_ERROR)

    return my_response(result=True, alert=response_messages.FEEDBACK_CREATE_SUCCESS)


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
        return my_response(alert=response_messages.UNEXPECTED_ERROR)

    return my_response(result=True, alert=response_messages.FEEDBACK_UPDATE_SUCCESS)


def delete_feedback(request, user_id=None):
    request_data = request.GET
    feedback_id = request_data['feedback_id']
    feedback_object = get_data(model=FeedbackMaster, filters={'id': feedback_id})
    if not feedback_object:
        return my_response(alert=response_messages.FEEDBACK_NOT_EXIST)

    feedback_object.delete()
    return my_response(result=True, alert=response_messages.FEEDBACK_DELETE_SUCCESS)