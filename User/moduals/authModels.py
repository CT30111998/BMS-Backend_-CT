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


def create_my_user(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    if request.method == constant.POST:
        # TIME_ZONE = pytz.timezone('Asia/Kolkata')
        # Current_data_time = datetime.now(TIME_ZONE)
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
            alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.USER_MODEL_FIELDS['first_name']}, \
{constant.USER_MODEL_FIELDS['last_name']},\
{constant.USER_MODEL_FIELDS['email']},\
{constant.USER_MODEL_FIELDS['mobile_number']},\
{constant.USER_MODEL_FIELDS['password']} and \
{constant.USER_MODEL_FIELDS['confirm_password']} \
in {constant.PAYLOAD_DATA_FORMAT}"
            return create_response(result=False, alert=alert)
        # created_at = Current_data_time
        # updated_at = Current_data_time

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
        try:
            create_user = AuthUser.objects.create_user(username=user_email, email=user_email, password=password)
            create_user.first_name = first_name
            create_user.last_name = last_name
            success = create_user.save()
            get_data = AuthUser.objects.get(username=user_email)
            get_id = get_data.id
        except:
            alert = constant.USER_EXIST_MASSAGE
            result = False
            return create_response(result=result, alert=alert)
        if get_id:
            user_detail = UserDetail()
            user_detail.firstName = first_name
            user_detail.lastName = last_name
            user_detail.empNo = get_id
            user_detail.mNo = mobile_no
            user_detail.email = user_email
            user_detail.user = create_user
            save = user_detail.save()

            user_permission = userPermission()
            user_permission.user = create_user
            user_permission.save()

            alert = constant.REGISTER_SUCCESSFUL
            result = True
            data = {'id': get_id}
            return create_response(alert=alert, result=result, data=data)
    alert = constant.REGISTER_FAIL
    result = False
    return create_response(result=result, alert=alert)


def user_login(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    if request.method == constant.POST:
        try:
            get_request_data = loads(request.body)
            user_email, password = \
                get_request_data[constant.USER_MODEL_FIELDS['email']], \
                get_request_data[constant.USER_MODEL_FIELDS['password']]
        except:
            result = False
            alert = f"{constant.PAYLOAD_DATA_ERROR} {constant.USER_MODEL_FIELDS['email']} &\
{constant.USER_MODEL_FIELDS['password']} {constant.PAYLOAD_DATA_FORMAT}"
            return create_response(alert=alert, result=result)
        field = [user_email, password]
        fields_check = null_valid(field)
        if not fields_check:
            result = False
            alert = constant.ALL_FIELD_REQUIRE
            return create_response(alert=alert, result=result)

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
            alert = constant.LOGOUT_SUCCESSFUL
            result = True
            return create_response(alert=alert, result=result)
        except:
            alert = constant.LOGOUT_FAIL
            result = False
            return create_response(alert=alert, result=result)
    alert = constant.USER_NOT_LOGGED_IN
    result = False
    return create_response(alert=alert, result=result)


def user_profile(request=None, user_id=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    try:
        details = UserDetail.objects.get(user=user_id)
        if request.method == constant.GET:
            try:
                if details:
                    serialize = UserSerializer(details, many=False)
                    result = True
                    alert = constant.DATA_FETCH_SUCCESSFUL
                    return create_response(alert=alert, result=result, data=serialize.data)
                result = False
                alert = constant.DATA_FETCH_FAIL
                return create_response(alert=alert, result=result)
            except:
                result = False
                alert = constant.DATA_FETCH_FAIL
                return create_response(alert=alert, result=result)
    except Exception:
        result = False
        alert = constant.DATA_NOT_FOUND
        return create_response(alert=alert, result=result)

    if request.method == constant.PUT:
        alert = constant.UPLOAD_FAIL
        result = False
        file = request.FILES[constant.USER_MODEL_FIELDS['image']]
        details = UserDetail.objects.get(user=user_id)
        if file:
            fs = FileSystemStorage()
            path = constant.UPLOAD_PATH + constant.PROFILE_PATH + file.name
            fs.save(name=path, content=file)
            details.image = path
            details.save()
            alert = constant.UPDATE_SUCCESSFUL
            result = True
        serialize = UserSerializer(details, many=False)
        return create_response(result=result, alert=alert, data=serialize.data)
