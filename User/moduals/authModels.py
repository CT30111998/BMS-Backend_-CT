from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User as AuthUser
from ..models import UserMaster as UserDetail, BmsSession as bmSession, UserPermission as userPermission
from django.contrib.auth import login, authenticate
from django.contrib import auth
from BMSystem import constants
from User.serializers import UserSerializer as UserSer, UserPermissionSerializer as PermissionSer
from json import loads
from BMSystem.base_function import \
    create_response as my_response_create, \
    get_session as my_session_get, \
    get_payload_error_alert as my_payload_error, \
    pass_valid as my_pass_valid, \
    null_valid, create_session as my_session_create


def get_all_user_data(request):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)
    get_users = UserDetail.objects.all()
    serialize = UserSer(get_users, many=True)
    data = serialize.data
    return my_response_create(result=True, alert=constants.DATA_FETCH_SUCCESSFUL, data=data)


def create_my_user(request=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # print("USER ID: ", user_id)
    # if user_id:
    #     return my_response_create(result=False, alert=constants.USER_LOGGED_IN)
    if request.method == constants.POST:
        try:
            request_data = request.data
            first_name, last_name, user_email, mobile_no, password, confirm_password = \
                request_data[constants.USER_MODEL_FIELDS['first_name']].capitalize(), \
                request_data[constants.USER_MODEL_FIELDS['last_name']].capitalize(), \
                request_data[constants.USER_MODEL_FIELDS['email']], \
                request_data[constants.USER_MODEL_FIELDS['mobile_number']], \
                request_data[constants.USER_MODEL_FIELDS['password']], \
                request_data[constants.USER_MODEL_FIELDS['confirm_password']]
        except:
            alert = my_payload_error(
                constants.USER_MODEL_FIELDS['first_name'],
                constants.USER_MODEL_FIELDS['last_name'],
                constants.USER_MODEL_FIELDS['email'],
                constants.USER_MODEL_FIELDS['mobile_number'],
                constants.USER_MODEL_FIELDS['password'],
                constants.USER_MODEL_FIELDS['confirm_password']
            )
            return my_response_create(result=False, alert=alert)

        # Validation
        all_field = [first_name, last_name, user_email, mobile_no, password, confirm_password]

        valid_pass1 = my_pass_valid(password)
        valid_pass2 = my_pass_valid(confirm_password)
        if not valid_pass2 or not valid_pass1:
            alert = constants.PASSWORD_LENGTH_ALERT
            result = False
            return my_response_create(alert=alert, result=result)

        if password != confirm_password:
            alert = constants.PASSWORD_NOT_MATCH
            result = False
            return my_response_create(alert=alert, result=result)

        auth_user_params = {
            constants.USER_MODEL_FIELDS['username']: user_email,
            constants.USER_MODEL_FIELDS['email']: user_email,
            constants.USER_MODEL_FIELDS['password']: password,
            "first_name": first_name,
            "last_name": last_name
        }
        try:
            create_user = AuthUser.objects.create_user(**auth_user_params)
            success = create_user.save()
            get_data = AuthUser.objects.get(username=user_email)
            get_id = get_data.id
        except:
            alert = constants.USER_EXIST_MASSAGE
            result = False
            return my_response_create(result=result, alert=alert)
        if get_id:
            try:
                user_params = {
                    constants.USER_MODEL_FIELDS['first_name']: first_name,
                    constants.USER_MODEL_FIELDS['last_name']: last_name,
                    constants.USER_MODEL_FIELDS['employee_number']: get_id,
                    constants.USER_MODEL_FIELDS['mobile_number']: mobile_no,
                    constants.USER_MODEL_FIELDS['email']: user_email,
                    constants.USER_MODEL_FIELDS['user']: create_user,
                }
                user_detail = UserDetail(**user_params)
                save = user_detail.save()
            except:
                get_auth_user = AuthUser.objects.filter(id=get_id)
                get_auth_user.delete()
                return my_response_create(result=False, alert=constants.USER_CREATE_FAIL_USER_MASTER)
            try:
                user_permission = userPermission(**{constants.USER_MODEL_FIELDS['user']: create_user})
                user_permission.save()
            except:
                get_auth_user = AuthUser.objects.filter(id=get_id)
                get_user = UserDetail.objects.filter(**{constants.USER_MODEL_FIELDS['user']: get_id})
                get_auth_user.delete()
                get_user.delete()
                return my_response_create(result=False, alert=constants.USER_CREATE_FAIL_USER_PERMISSION)

            alert = constants.REGISTER_SUCCESSFUL
            data = {'id': get_id}
            return my_response_create(alert=alert, result=True, data=data)

    return my_response_create(result=False, alert=constants.REGISTER_FAIL)


def delete_user(request, get_user_id=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
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
    get_user = AuthUser.objects.filter(**{constants.USER_MODEL_FIELDS['id']: get_user_id})
    if not get_user:
        return my_response_create(result=False, alert=constants.USER_NOT_EXIST)
    get_user.delete()
    return my_response_create(result=True, alert=constants.DELETE_USER_SUCCESSFUL)


def user_login(request=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # user_id_session = bmSession.objects.filter(**{'sessionKey': constants.SESSION_USER_ID})
    #
    # if user_id or user_id_session:
    #     return my_response_create(result=False, alert=constants.USER_LOGGED_IN)
    if request.method == constants.POST:
        try:
            get_request_data = loads(request.body)
            user_email = get_request_data[constants.USER_MODEL_FIELDS['username']]
            password = get_request_data[constants.USER_MODEL_FIELDS['password']]

        except:
            alert = my_payload_error(constants.USER_MODEL_FIELDS['username'], constants.USER_MODEL_FIELDS['password'])
            return my_response_create(alert=alert, result=False)
        field = [user_email, password]
        fields_check = null_valid(field)
        if not fields_check:
            return my_response_create(alert=False, result=constants.ALL_FIELD_REQUIRE)

        pass_check = my_pass_valid(password)
        if not pass_check:
            result = False
            alert = constants.PASSWORD_LENGTH_ALERT
            return my_response_create(alert=alert, result=result)

        try:
            check_user = AuthUser.objects.get(email=user_email)
        except:
            return my_response_create(result=False, alert=constants.ACCOUNT_NOT_EXIST_WITH_EMAIL)

        user = authenticate(username=user_email, password=password)
        user_id = None

        if user is not None:
            login(request, user)
            get_user = AuthUser.objects.get(username=user)
            user_id = get_user.id
            if user_id is not None:
                my_session_create(request, constants.SESSION_USER_ID, user_id)
                session = bmSession(**{'sessionKey': constants.SESSION_USER_ID, 'sessionValue': user_id})
                session.save()
                get_user_role = userPermission.objects.get(user=user_id)
                serializer = PermissionSer(get_user_role, many=False)
                permission = serializer.data.get("permission")
                alert = constants.LOGIN_SUCCESSFUL
                result = True
                my_session_create(request, constants.SESSION_EMAIL, user_email)
                data = {"id": user_id, "role": get_user_role.permission}
                return my_response_create(alert=alert, result=result, data=data)
        result = False
        alert = constants.USER_AND_PASSWORD_NOT_MATCH
        return my_response_create(alert=alert, result=result)


def user_logout(request=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
    user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if user_id:
    #     return my_response_create(alert=constants.USER_NOT_LOGGED_IN, result=False)
    try:
        auth.logout(request)
        delete_session = bmSession.objects.filter(**{'sessionKey': constants.SESSION_USER_ID})
        delete_session.delete()
        return my_response_create(alert=constants.LOGOUT_SUCCESSFUL, result=True)
    except:
        return my_response_create(alert=constants.LOGOUT_FAIL, result=False)


def user_profile(request=None, user_id=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
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
        return my_response_create(alert=constants.DATA_NOT_FOUND, result=False)
        # if request.method == constants.GET:
    serialize = UserSer(details, many=False)
    return my_response_create(alert=constants.DATA_FETCH_SUCCESSFUL, result=True, data=serialize.data)


def update_profile(request, user_id=None):
    if not request:
        return my_response_create(result=False, alert=constants.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constants.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constants.USER_NOT_LOGGED_IN)

    file = request.FILES[constants.USER_MODEL_FIELDS['image']]
    try:
        details = UserDetail.objects.get(user=user_id)
    except:
        return my_response_create(result=False, alert=constants.DATA_NOT_FOUND)
    if not file:
        return my_response_create(result=False, alert=constants.UPLOAD_FAIL)
    fs = FileSystemStorage()
    path = f"{constants.UPLOAD_PATH}{constants.PROFILE_PATH}{file.name}"
    fs.save(name=path, content=file)
    details.update(**{constants.USER_MODEL_FIELDS["image"]: path})
    details.save()
    serialize = UserSer(details, many=False)
    return my_response_create(result=True, alert=constants.UPDATE_SUCCESSFUL, data=serialize.data)
