from re import template
from urllib import request
from ..models import User as UserDetail
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import render
from . import MySession
from .Validation import Validation
from BMSystem import constant as set
from User.serializers import *
from rest_framework import response
from ..form import profileUpload
from django.core.files.storage import FileSystemStorage


class authUser:

    def createMyUser(self, request):
        if request.method == 'POST':
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
                alert = "All fields required"
                result = False
                send = {"result": result, "alert": alert}
                return send
                # return render(request, "register.html", {"fail": alert})

            validPass1 = Validation().passValid(password)
            validPass2 = Validation().passValid(password1)
            if not validPass2 or not validPass1:
                alert = "Password should have min 8 characters"
                result = False
                send = {"result": result, "alert": alert}
                return send
                # return redirect("register/")
                # return render(request, "register.html", {"fail": alert})

            if password != password1:
                alert = "Password does not match"
                result = False
                send = {"result": result, "alert": alert}
                return send
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
            alert = "Account create successful"
            result = True
            data = {'id': getId}
            send = {"result": result, "alert": alert, 'data': data}
            return (send)
            # return render(request, 'login.html', {"success": alert})

    def Login(self, request):
        if request.method == 'POST':
            email = request.POST[set.USER_MODEL_FIELDS['email']]
            password = request.POST[set.USER_MODEL_FIELDS['password']]
            fields = [email, password]
            fieldsCheck = Validation().nullValid(fields)
            if not fieldsCheck:
                result = False
                alert = "All field required"
                send = {"result": result, "alert": alert}
                return send

            passCheck = Validation().passValid(password)
            if not passCheck:
                result = False
                alert = "Password should have minimum 8 character"
                send = {"result": result, "alert": alert}
                return send

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
                    alert = "Login Successful"
                    result = True
                    MySession.createSession(request, 'email', email)
                    serializer = UserSerializer(get_user_data, many=False)
                    send = {"result": result, "alert": alert, 'data': serializer.data}
                    return (send)
            result = False
            alert = "Email and password could not match"
            send = {"result": result, "alert": alert}
            return send


    def Profile(request):
        details = UserDetail.objects.get(id=request.session['userId']) 
        return details

    def updateProfile(request):
        if request.method == 'POST':
            details = UserDetail.objects.get(id=request.session['userId'])
            result = 'File could not upload! try again later'
            file = request.FILES['image1']
            if file:  
                fs = FileSystemStorage()
                path = set.UPLOAD_PATH+set.PROFILE_PATH+file.name
                fs.save(name=path, content=file,)
                details.image = path
                details.save()  
                result = "Update successfull!"
            return result


            # except Exception as ex:
            #     result = "Could not update try again!"
            #     return result