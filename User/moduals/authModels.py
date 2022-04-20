from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User as AuthUser
from ..models import UserMaster as UserDetail
from ..models import UserPermission as userPermission
from django.contrib.auth import login, authenticate
from django.contrib import auth
from BMSystem import constant
from User.serializers import *
from json import loads, dumps
from BMSystem.base_function import *


def get_all_user_data(request):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request, constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    get_users = UserMaster.objects.all()
    serialize = UserSerializer(get_users, many=True)
    data = serialize.data
    return create_response(result=True, alert=constant.DATA_FETCH_SUCCESSFUL, data=data)


def create_my_user(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    if request.method == constant.POST:
        try:
            request_data = loads(request.body)
            first_name, last_name, user_email, mobile_no, password, confirm_password = \
                request_data[constant.USER_MODEL_FIELDS['first_name']].capitalize(), \
                request_data[constant.USER_MODEL_FIELDS['last_name']].capitalize(), \
                request_data[constant.USER_MODEL_FIELDS['email']], \
                request_data[constant.USER_MODEL_FIELDS['mobile_number']], \
                request_data[constant.USER_MODEL_FIELDS['password']], \
                request_data[constant.USER_MODEL_FIELDS['confirm_password']]
        except:
            alert = get_payload_error_alert(
                constant.USER_MODEL_FIELDS['first_name'],
                constant.USER_MODEL_FIELDS['last_name'],
                constant.USER_MODEL_FIELDS['email'],
                constant.USER_MODEL_FIELDS['mobile_number'],
                constant.USER_MODEL_FIELDS['password'],
                constant.USER_MODEL_FIELDS['confirm_password']
            )
            return create_response(result=False, alert=alert)

        # Validation
        all_field = [first_name, last_name, user_email, mobile_no, password, confirm_password]
        valid = null_valid(all_field)
        if not valid:
            alert = constant.ALL_FIELD_REQUIRE
            result = False
            return create_response(alert=alert, result=result)

        valid_pass1 = pass_valid(password)
        valid_pass2 = pass_valid(confirm_password)
        if not valid_pass2 or not valid_pass1:
            alert = constant.PASSWORD_LENGTH_ALERT
            result = False
            return create_response(alert=alert, result=result)

        if password != confirm_password:
            alert = constant.PASSWORD_NOT_MATCH
            result = False
            return create_response(alert=alert, result=result)

        auth_user_params = {
            constant.USER_MODEL_FIELDS['username']: user_email,
            constant.USER_MODEL_FIELDS['email']: user_email,
            constant.USER_MODEL_FIELDS['password']: password,
            "first_name": first_name,
            "last_name": last_name
        }
        try:
            create_user = AuthUser.objects.create_user(**auth_user_params)
            success = create_user.save()
            get_data = AuthUser.objects.get(username=user_email)
            get_id = get_data.id
        except:
            alert = constant.USER_EXIST_MASSAGE
            result = False
            return create_response(result=result, alert=alert)
        if get_id:
            try:
                user_params = {
                    constant.USER_MODEL_FIELDS['first_name']: first_name,
                    constant.USER_MODEL_FIELDS['last_name']: last_name,
                    constant.USER_MODEL_FIELDS['employee_number']: get_id,
                    constant.USER_MODEL_FIELDS['mobile_number']: mobile_no,
                    constant.USER_MODEL_FIELDS['email']: user_email,
                    constant.USER_MODEL_FIELDS['user']: create_user,
                }
                user_detail = UserDetail(**user_params)
                save = user_detail.save()
            except:
                get_auth_user = AuthUser.objects.filter(id=get_id)
                get_auth_user.delete()
                return create_response(result=False, alert=constant.USER_CREATE_FAIL_USER_MASTER)
            try:
                user_permission = userPermission(**{constant.USER_MODEL_FIELDS['user']: create_user})
                user_permission.save()
            except:
                get_auth_user = AuthUser.objects.filter(id=get_id)
                get_user = UserMaster.objects.filter(**{constant.USER_MODEL_FIELDS['user']: get_id})
                get_auth_user.delete()
                get_user.delete()
                return create_response(result=False, alert=constant.USER_CREATE_FAIL_USER_PERMISSION)

            alert = constant.REGISTER_SUCCESSFUL
            data = {'id': get_id}
            return create_response(alert=alert, result=True, data=data)

    return create_response(result=False, alert=constant.REGISTER_FAIL)


def delete_user(request):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request, constant.SESSION_USER_ID)

    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    if not request.body:
        alert = get_payload_error_alert(constant.USER_MODEL_FIELDS['get_user_id'])
        return create_response(result=False, alert=alert)

    get_json_data = loads(request.body)

    if constant.USER_MODEL_FIELDS['get_user_id'] not in get_json_data:
        alert = get_payload_error_alert(constant.USER_MODEL_FIELDS['get_user_id'])
        return create_response(result=False, alert=alert)
    get_user_id = get_json_data[constant.USER_MODEL_FIELDS['get_user_id']]
    get_user = AuthUser.objects.filter(**{constant.USER_MODEL_FIELDS['id']: get_user_id})
    if not get_user:
        return create_response(result=False, alert=constant.USER_NOT_EXIST)
    get_user.delete()
    return create_response(result=True, alert=constant.DELETE_USER_SUCCESSFUL)


def user_login(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    if request.method == constant.POST:
        try:
            get_request_data = loads(request.body)
            user_email = get_request_data[constant.USER_MODEL_FIELDS['email']]
            password = get_request_data[constant.USER_MODEL_FIELDS['password']]

        except:
            alert = get_payload_error_alert(constant.USER_MODEL_FIELDS['email'], constant.USER_MODEL_FIELDS['password'])
            return create_response(alert=alert, result=False)
        field = [user_email, password]
        fields_check = null_valid(field)
        if not fields_check:
            return create_response(alert=False, result=constant.ALL_FIELD_REQUIRE)

        pass_check = pass_valid(password)
        if not pass_check:
            result = False
            alert = constant.PASSWORD_LENGTH_ALERT
            return create_response(alert=alert, result=result)

        user = authenticate(username=user_email, password=password)
        user_id = None

        if user is not None:
            login(request, user)
            get_user = AuthUser.objects.get(username=user)
            user_id = get_user.id
            if user_id is not None:
                create_session(request, constant.SESSION_USER_ID, user_id)
                get_user_role = userPermission.objects.get(user=user_id)
                serializer = UserPermissionSerializer(get_user_role, many=False)
                permission = serializer.data.get("permission")
                alert = constant.LOGIN_SUCCESSFUL
                result = True
                create_session(request, constant.SESSION_EMAIL, user_email)
                data = {"id": user_id, "role": get_user_role.permission}
                return create_response(alert=alert, result=result, data=data)
        result = False
        alert = constant.USER_AND_PASSWORD_NOT_MATCH
        return create_response(alert=alert, result=result)


def user_logout(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user = get_session(request, constant.SESSION_USER_ID)
    if user:
        try:
            auth.logout(request)
            return create_response(alert=constant.LOGOUT_SUCCESSFUL, result=True)
        except:
            return create_response(alert=constant.LOGOUT_FAIL, result=False)

    return create_response(alert=constant.USER_NOT_LOGGED_IN, result=False)


def user_profile(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    try:
        details = UserDetail.objects.get(user=user_id)
    except Exception:
        return create_response(alert=constant.DATA_NOT_FOUND, result=False)

    if request.method == constant.GET:
        serialize = UserSerializer(details, many=False)
        return create_response(alert=constant.DATA_FETCH_SUCCESSFUL, result=True, data=serialize.data)


def update_profile(request):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    file = request.FILES[constant.USER_MODEL_FIELDS['image']]
    try:
        details = UserDetail.objects.get(user=user_id)
    except:
        return create_response(result=False, alert=constant.DATA_NOT_FOUND)
    if not file:
        return create_response(result=False,  alert=constant.UPLOAD_FAIL)
    fs = FileSystemStorage()
    path = f"{constant.UPLOAD_PATH}{constant.PROFILE_PATH}{file.name}"
    fs.save(name=path, content=file)
    details.update(**{constant.USER_MODEL_FIELDS["image"]: path})
    details.save()
    serialize = UserSerializer(details, many=False)
    return create_response(result=True, alert=constant.UPDATE_SUCCESSFUL, data=serialize.data)
