from django.core.files.storage import FileSystemStorage
from Auth.models import AuthMaster as AuthUser
from ..models import UserMaster as UserDetail
from BMSystem import constants, response_messages, model_fields
from User.serializers import UserSerializer as UserSer
from base.common_helpers import create_response as my_response_create


def get_all_user_data(request):
    if not request:
        return my_response_create(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)
    get_users = UserDetail.objects.all()
    serialize = UserSer(get_users, many=True)
    data = serialize.data
    return my_response_create(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=data)


def delete_user(request, get_user_id=None):
    if not request:
        return my_response_create(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # if not request.body:
    #     alert = my_payload_error(constants.USER_MODEL_FIELDS['get_user_id'])
    #     return my_response_create(result=False, alert=alert)
    #
    # get_json_data = loads(request.body)
    #
    # if constants.USER_MODEL_FIELDS['get_user_id'] not in get_json_data:
    #     alert = my_payload_error(constants.USER_MODEL_FIELDS['get_user_id'])
    #     return my_response_create(result=False, alert=alert)
    # get_user_id = get_json_data[constants.USER_MODEL_FIELDS['get_user_id']]
    get_user = AuthUser.objects.filter(**{model_fields.ID: get_user_id})
    if not get_user:
        return my_response_create(result=False, alert=response_messages.USER_NOT_EXIST)
    get_user.delete()
    return my_response_create(result=True, alert=response_messages.DELETE_USER_SUCCESSFUL)


def user_profile(request=None, user_id=None):
    if not request:
        return my_response_create(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constants.SESSION_USER_ID)
    # try:
    #     # user_id = loads(request.body)['user_id']
    # except:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)
    # if not user_id:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)
    try:
        details = UserDetail.objects.get(user=user_id)
    except Exception:
        return my_response_create(alert=response_messages.DATA_NOT_FOUND, result=False)
        # if request.method == constants.GET:
    serialize = UserSer(details, many=False)
    return my_response_create(alert=response_messages.DATA_FETCH_SUCCESSFUL, result=True, data=serialize.data)


def update_profile(request, user_id=None):
    if not request:
        return my_response_create(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)

    file = request.FILES[model_fields.IMAGE]
    try:
        details = UserDetail.objects.get(user=user_id)
    except:
        return my_response_create(result=False, alert=response_messages.DATA_NOT_FOUND)
    if not file:
        return my_response_create(result=False, alert=response_messages.UPLOAD_FAIL)
    fs = FileSystemStorage()
    path = f"{constants.UPLOAD_PATH}{constants.PROFILE_PATH}{file.name}"
    fs.save(name=path, content=file)
    details.update(**{model_fields.IMAGE: path})
    details.save()
    serialize = UserSer(details, many=False)
    return my_response_create(result=True, alert=response_messages.UPDATE_SUCCESSFUL, data=serialize.data)
