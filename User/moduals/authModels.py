from django.core.files.storage import FileSystemStorage

from ..models import User as UserDetail
from django.contrib.auth import login, authenticate
from django.contrib import auth
from . import MySession
from .Validation import Validation
from BMSystem import constant as set
from User.serializers import *
from BMSystem.base_function import *


def create_my_user(request):
    if request.method == set.POST:
        # TIME_ZONE = pytz.timezone('Asia/Kolkata')
        # Current_data_time = datetime.now(TIME_ZONE)
        fName = request.POST[set.USER_MODEL_FIELDS['first_name']]
        lName = request.POST[set.USER_MODEL_FIELDS['last_name']]
        email = request.POST[set.USER_MODEL_FIELDS['email']]
        mNo = request.POST[set.USER_MODEL_FIELDS['mobile_number']]
        password = request.POST.get(set.USER_MODEL_FIELDS['password'])
        password1 = request.POST.get(set.USER_MODEL_FIELDS['confirm_password'])
        # created_at = Current_data_time
        # updated_at = Current_data_time
        # Validation
        fields = [fName, lName, email, mNo, password, password1]
        valid = Validation().nullValid(fields)
        if not valid:
            alert = set.ALL_FIELD_REQUIRE
            result = False
            return create_response(alert=alert, result=result)
            # return render(request, "register.html", {"fail": alert})
        validPass1 = Validation().passValid(password)
        validPass2 = Validation().passValid(password1)
        if not validPass2 or not validPass1:
            alert = set.PASSWORD_LENGTH_ALERT
            result = False
            return create_response(alert=alert, result=result)
            # return redirect("register/")
            # return render(request, "register.html", {"fail": alert})
        if password != password1:
            alert = set.PASSWORD_NOT_MATCH
            result = False
            return create_response(alert=alert, result=result)
            # return redirect("register/")
            # return render(request, "register.html", {"fail": alert})
        # try:
        createUser = User.objects.create_user(username=email, email=email, password=password)
        createUser.first_name = fName
        createUser.last_name = lName
        success = createUser.save()
        getData = User.objects.get(username=email)
        getId = getData.id
        # except:
        #     alert = "Already have account with this email"
        #     result = False
        #     send = {"result": result, "alert": alert}
        #     return send
        #     # return render(request, 'login.html', {"fail": alert})
        userDetail = UserDetail()
        userDetail.firstName = fName
        userDetail.lastName = lName
        userDetail.empNo = getId
        # userDetail.user = int(getId)
        userDetail.mNo = mNo
        userDetail.email = email
        save = userDetail.save()
        userName = createUser.get_username()
        # try:
        # Successful create
        alert = set.REGISTER_SUCCESSFUL
        result = True
        data = {'id': getId}
        return create_response(alert=alert, result=result, data=data)
        # return render(request, 'login.html', {"success": alert})


def user_login(request):
    if request.method == set.POST:
        email = request.POST[set.USER_MODEL_FIELDS['email']]
        password = request.POST[set.USER_MODEL_FIELDS['password']]
        fields = [email, password]
        fieldsCheck = Validation().nullValid(fields)
        if not fieldsCheck:
            result = False
            alert = set.ALL_FIELD_REQUIRE
            send = {"result": result, "alert": alert}
            return create_response(alert=alert, result=result)

        passCheck = Validation().passValid(password)
        if not passCheck:
            result = False
            alert = set.PASSWORD_LENGTH_ALERT
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
                MySession.createSession(request, 'userId', userId)
                alert = set.LOGIN_SUCCESSFUL
                result = True
                MySession.createSession(request, 'email', email)
                # serializer = UserSerializer(get_user_data, many=False)
                data = {'id': userId}
                return create_response(alert=alert, result=result, data=data)
        result = False
        alert = set.USER_AND_PASSWORD_NOT_MATCH
        return create_response(alert=alert, result=result)


def user_logout(request):
    try:
        auth.logout(request)
        alert = set.LOGOUT_SUCCESSFUL
        result = True
        return create_response(alert=alert, result=result)
    except:
        alert = set.LOGOUT_FAIL
        result = False
        return create_response(alert=alert, result=result)


def user_profile(request, user_id=None):
    details = UserDetail.objects.get(id=user_id)
    if request.method == set.GET:
        try:
            if details:
                serialize = UserSerializer(details, many=False)
                result = True
                alert = set.DATA_FETCH_SUCCESSFUL
                return create_response(alert=alert, result=result, data=serialize.data)
            result = False
            alert = set.DATA_FETCH_FAIL
            return create_response(alert=alert, result=result)
        except:
            result = False
            alert = set.DATA_FETCH_FAIL
            return create_response(alert=alert, result=result)

    if request.method == set.PUT:
        alert = set.UPLOAD_FAIL
        result = False
        file = request.FILES['image1']
        if file:
            fs = FileSystemStorage()
            path = set.UPLOAD_PATH + set.PROFILE_PATH + file.name
            fs.save(name=path, content=file)
            details.image = path
            details.save()
            alert = set.UPDATE_SUCCESSFUL
            result = True
        details = UserDetail.objects.get(id=user_id)
        serialize = UserSerializer(details, many=False)
        return create_response(result=result, alert=alert, data=serialize.data)
