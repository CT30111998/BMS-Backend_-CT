from BMSystem.base_function import \
    get_session as my_session_get, \
    get_name_from_master_user as my_name_create, \
    get_payload_error_alert as my_payload_error, \
    get_date_from_tabl_object as my_date_get_from_table
from BMSystem import constants, response_messages, model_fields, decimal_constants
from base.common_helpers import create_response as my_response
from json import loads
from Auth.models import AuthMaster as AuthUser
from User.models import UserMaster as MasterUser
from .models import AttendanceMaster as AttendMaster, FeedbackMaster
from .serializers import AttendanceSerializer
from django.utils import timezone
from base.query_modules import save_data, get_data, update_data_by_fields, update_data_by_filters
from datetime import datetime


def get_all_user_attendance(request_data=None):
    attend_filter = {}
    order_by = f"-{model_fields.DATE}"

    if model_fields.YEAR in request_data:
        attend_filter[model_fields.YEAR] = request_data[
            model_fields.YEAR
        ]
        if model_fields.MONTH in request_data:
            attend_filter[model_fields.MONTH] = request_data[
                model_fields.MONTH
            ]
            if model_fields.DAY in request_data:
                attend_filter[model_fields.DAY] = request_data[
                    model_fields.DAY
                ]

    if (model_fields.MONTH in request_data and
        model_fields.YEAR not in request_data) \
            or (model_fields.DAY in request_data and
                model_fields.MONTH not in request_data):
        alert = my_payload_error(model_fields.YEAR, model_fields.MONTH)
        return my_response(result=False, alert=alert)

    if model_fields.DATE in request_data:
        attend_filter[model_fields.DATE] = request_data[
            model_fields.DATE
        ]

    if model_fields.ORDER_BY in request_data:
        if request_data[model_fields.ORDER_BY] == decimal_constants.ORDER_BY_DATE_ASCENDING:
            order_by = model_fields.DATE

    attendance_object = get_data(model=AttendMaster, filters=attend_filter, order_by=order_by)
    serializer_object = AttendanceSerializer(attendance_object, many=True)

    if not attendance_object:
        return my_response(alert=response_messages.ATTEND_NOT_FOUND)

    return my_response(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=serializer_object.data)


def get_user_attendance(attend_id=None, user_id=None):

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


def create_user_attendance(request_data=None, user_id=None):

    if model_fields.PUNCH_STATUS not in request_data:
        alert = f"{response_messages.PAYLOAD_DATA_ERROR} {model_fields.PUNCH_STATUS}" + \
                f" in {response_messages.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)

    emp_id = request_data.get('emp_id', None)
    user_object = get_data(model=AuthUser, filters={model_fields.ID: emp_id if emp_id else user_id})
    if not user_object:
        return my_response(alert=response_messages.USER_NOT_EXIST)

    attend_params = {model_fields.USER: user_object.first()}

    if int(request_data[model_fields.PUNCH_STATUS]) == decimal_constants.PUNCH_IN_STATUS:
        attend_params[model_fields.PUNCH_IN] = datetime.now().time()
    else:
        attend_params[model_fields.PUNCH_OUT] = datetime.now().time()

    if model_fields.ATTEND_ID not in request_data:
        attend_params.update({
            model_fields.DAY: datetime.now().date().day,
            model_fields.MONTH: datetime.now().date().month,
            model_fields.YEAR: datetime.now().date().year,
            model_fields.CREATED_BY: user_object.first(),
            model_fields.CREATED_AT: timezone.now()
        })

        save_data(model=AttendMaster, fields=attend_params)
        alert = response_messages.CREATE_ATTENDANCE_SUCCESSFUL
    else:
        attend_object = get_data(model=AttendMaster, filters={model_fields.ID: request_data[model_fields.ATTEND_ID]})
        if not attend_object:
            return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)

        attend_params.update({
            model_fields.UPDATED_BY: user_object.first(),
            model_fields.UPDATED_AT: timezone.now()
        })

        update_data_by_fields(model_object=attend_object, fields=attend_params)
        alert = response_messages.UPDATE_ATTENDANCE_SUCCESSFUL

    return my_response(result=True, alert=alert)


# def update_user_attendance(request=None):
#     if not request:
#         return my_response(result=False, alert=constants.UNEXPECTED_ERROR)
#     return my_response(result=True, alert=constants.UPDATE_ATTENDANCE_SUCCESSFUL)


def delete_user_attendance(request_data=None):
    if model_fields.ATTEND_ID not in request_data:
        alert = f"{response_messages.PAYLOAD_DATA_ERROR} {model_fields.ATTEND_ID}" + \
                f" in {response_messages.PAYLOAD_DATA_FORMAT}"
        return my_response(result=False, alert=alert)

    attend_object = get_data(model=AttendMaster, filters={model_fields.ID: request_data[model_fields.ATTEND_ID]})
    if not attend_object:
        return my_response(result=False, alert=response_messages.ATTEND_NOT_FOUND)

    attend_object.delete()
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


def get_feedback(request_data):
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


def create_feedback(request_data, user_id=None):
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


def update_feedback(request_data):
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


def delete_feedback(request_data):
    request_data = request_data.GET
    feedback_id = request_data['feedback_id']
    feedback_object = get_data(model=FeedbackMaster, filters={'id': feedback_id})
    if not feedback_object:
        return my_response(alert=response_messages.FEEDBACK_NOT_EXIST)

    feedback_object.delete()
    return my_response(result=True, alert=response_messages.FEEDBACK_DELETE_SUCCESS)
