from django.core.files.storage import FileSystemStorage
from Auth.models import AuthMaster as AuthUser
from ..models import UserMaster
from base.query_modules import get_data, save_data, update_data_by_fields
from BMSystem import constants, response_messages, model_fields, decimal_constants
from User.serializers import UserSerializer as UserSer
from base.common_helpers import create_response as my_response_create


def get_all_user_data(request_data=None):
    user_id = request_data.get('user_id', None)
    user_filter = {
        model_fields.IS_DELETED: decimal_constants.NOT_DELETED,
    }
    if user_id:
        user_filter[model_fields.USER] = user_id
    user_object = get_data(model=UserMaster, filters=user_filter)

    if not user_object:
        return my_response_create(alert=response_messages.USER_NOT_EXIST)
    if len(user_object) == 1:
        serialize = UserSer(user_object[0], many=False)
    else:
        serialize = UserSer(user_object, many=True)
    return my_response_create(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=serialize.data)


def delete_user(user_id=None):

    user_object = get_data(model=UserMaster, filters={model_fields.USER: user_id})
    if not user_object:
        return my_response_create(alert=response_messages.USER_NOT_EXIST)
    user_object.update({model_fields.IS_DELETED: decimal_constants.DELETED})

    auth_user_object = get_data(model=AuthUser, filters={model_fields.ID: user_id})
    if not auth_user_object:
        return my_response_create(result=False, alert=response_messages.USER_NOT_EXIST)
    auth_user_object.update({model_fields.IS_DELETED: decimal_constants.DELETED})

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
        details = UserMaster.objects.get(user=user_id)
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
        user = UserMaster.objects.get(user=user_id)
    except:
        return my_response_create(result=False, alert=response_messages.DATA_NOT_FOUND)
    if not file:
        return my_response_create(result=False, alert=response_messages.UPLOAD_FAIL)
    fs = FileSystemStorage()
    path = f"{constants.UPLOAD_PATH}{constants.PROFILE_PATH}{file.name}"
    fs.save(name=path, content=file)
    # update_data_by_fields(model_object=)
    # details.update(**{model_fields.IMAGE: path})
    # details.save()
    # serialize = UserSer(details, many=False)
    return my_response_create(result=True, alert=response_messages.UPDATE_SUCCESSFUL, data=serialize.data)
