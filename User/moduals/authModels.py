from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User as AuthUser
from ..models import UserMaster as UserDetail
from ..models import UserPermission as userPermission
from django.contrib.auth import login, authenticate
from django.contrib import auth
from . import MySession
from .Validation import Validation
from BMSystem import constant
from User.serializers import *
from BMSystem.base_function import *


def create_my_user(request):
    if request.method == constant.POST:
        # TIME_ZONE = pytz.timezone('Asia/Kolkata')
        # Current_data_time = datetime.now(TIME_ZONE)
        fName = request.POST[constant.USER_MODEL_FIELDS['first_name']]
        lName = request.POST[constant.USER_MODEL_FIELDS['last_name']]
        email = request.POST[constant.USER_MODEL_FIELDS['email']]
        mNo = request.POST[constant.USER_MODEL_FIELDS['mobile_number']]
        password = request.POST.get(constant.USER_MODEL_FIELDS['password'])
        password1 = request.POST.get(constant.USER_MODEL_FIELDS['confirm_password'])
        # created_at = Current_data_time
        # updated_at = Current_data_time
        # Validation
        fields = [fName, lName, email, mNo, password, password1]
        valid = null_valid(fields)
        if not valid:
            alert = constant.ALL_FIELD_REQUIRE
            result = False
            return create_response(alert=alert, result=result)

        validPass1 = pass_valid(password)
        validPass2 = pass_valid(password1)
        if not validPass2 or not validPass1:
            alert = constant.PASSWORD_LENGTH_ALERT
            result = False
            return create_response(alert=alert, result=result)

        if password != password1:
            alert = constant.PASSWORD_NOT_MATCH
            result = False
            return create_response(alert=alert, result=result)
        try:
            createUser = AuthUser.objects.create_user(username=email, email=email, password=password)
            createUser.first_name = fName
            createUser.last_name = lName
            success = createUser.save()
            getData = AuthUser.objects.get(username=email)
            getId = getData.id
        except:
            alert = constant.USER_EXIST_MASSAGE
            result = False
            return create_response(result=result, alert=alert)
        if getId:
            userDetail = UserDetail()
            userDetail.firstName = fName
            userDetail.lastName = lName
            userDetail.empNo = getId
            # userDetail.user = int(getId)
            userDetail.mNo = mNo
            userDetail.email = email
            userDetail.user = createUser
            save = userDetail.save()
            user_permission = userPermission()
            user_permission.user = createUser
            user_permission.save()
            alert = constant.REGISTER_SUCCESSFUL
            result = True
            data = {'id': getId}
            return create_response(alert=alert, result=result, data=data)
    alert = constant.REGISTER_FAIL
    result = False
    return create_response(result=result, alert=alert)


def user_login(request):
    if request.method == constant.POST:
        email = request.POST[constant.USER_MODEL_FIELDS['email']]
        password = request.POST[constant.USER_MODEL_FIELDS['password']]
        fields = [email, password]
        fieldsCheck = null_valid(fields)
        if not fieldsCheck:
            result = False
            alert = constant.ALL_FIELD_REQUIRE
            send = {"result": result, "alert": alert}
            return create_response(alert=alert, result=result)

        passCheck = pass_valid(password)
        if not passCheck:
            result = False
            alert = constant.PASSWORD_LENGTH_ALERT
            send = {"result": result, "alert": alert}
            return create_response(alert=alert, result=result)

        user = authenticate(username=email, password=password)
        userId = None

        if user is not None:
            login(request, user)
            get_user = AuthUser.objects.get(username=user)
            get_user_data = UserDetail.objects.get(email=get_user.email)
            userId = get_user.id
            # request.session['username'] = userId
            if userId is not None:
                create_session(request, 'userId', userId)
                get_user_role = UserPermission.objects.get(user=userId)
                alert = constant.LOGIN_SUCCESSFUL
                result = True
                create_session(request, 'email', email)
                data = {'id': userId, 'role': get_user_role.permission}
                return create_response(alert=alert, result=result, data=data)
        result = False
        alert = constant.USER_AND_PASSWORD_NOT_MATCH
        return create_response(alert=alert, result=result)


def user_logout(request):
    user = get_session(request, 'userId')
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


def user_profile(request, user_id=None):
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
