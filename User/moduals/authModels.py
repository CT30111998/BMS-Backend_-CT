from ..models import User as UserDetail
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from . import MySession
from .Validation import Validation

class authUser:
    def createMyUser(self, request):
        if request.method == 'POST':
            # TIME_ZONE = pytz.timezone('Asia/Kolkata')
            # Current_data_time = datetime.now(TIME_ZONE)

            fName = request.POST['fName']
            lName = request.POST['lName']
            email = request.POST['email']
            mNo = request.POST['mNo']
            password = request.POST.get('pass')
            password1 = request.POST.get('pass1')
            # created_at = Current_data_time
            # updated_at = Current_data_time

            # Validation
            fields = [fName, lName, email, mNo, password, password1]
            valid = Validation().nullValid(fields)
            if not valid:
                alert = "All fields required"
                result = False
                send = [result, alert]
                return send
                # return render(request, "register.html", {"fail": alert})

            validPass1 = Validation().passValid(password)
            validPass2 = Validation().passValid(password1)
            if not validPass2 or not validPass1:
                alert = "Password should have min 8 characters"
                result = False
                send = [result, alert]
                return send
                # return redirect("register/")
                # return render(request, "register.html", {"fail": alert})

            if password != password1:
                alert = "Password does not match"
                result = False
                send = [result, alert]
                return send
                # return redirect("register/")
                # return render(request, "register.html", {"fail": alert})
            try:
                createUser = User.objects.create_user(username=email, email=email, password=password)
                createUser.first_name = fName
                createUser.last_name = lName
                success = createUser.save()
                getData = User.objects.get(username=email)
                getId = getData.id
            except:
                alert = "Already have account with this email"
                result = False
                send = [result, alert]
                return send
                # return render(request, 'login.html', {"fail": alert})

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
                

            # except:
            #     try:
            #         record = createUser.objects.get(id=getId)
            #         record.delete()
            #         alert = "Account create failed! Try again...1"
            #         result = False
            #         send = [result, alert]
            #         return send
            #         # return render(request, 'login.html', {"fail": alert})
            #     except:

            #         alert = "Account create failed! Try again..."
            #         result = False
            #         send = [result, alert]
            #         return send
            #         # return render(request, 'login.html', {"fail": alert})

            # Successful create
            alert = "Account create successful"
            result = True
            send = [result, alert]
            return send
            # return render(request, 'login.html', {"success": alert})

        else:
            alert = "Could not register"
            result = False
            send = [result, alert]
            return send

        
    def Login(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['pass']
            fields = [email, password]
            fieldsCheck = Validation().nullValid(fields)
            if not fieldsCheck:
                result = False
                alert = "All field required"
                send = [result, alert]
                return send

            passCheck = Validation().passValid(password)
            if not passCheck:
                result = False
                alert = "Password should have minimum 8 character"
                send = [result, alert]
                return send

            user = authenticate(username=email, password=password)
            userId = None

            if user is not None:
                login(request, user)
                userData = User.objects.get(username=user)
                userId = userData.id
                # request.session['username'] = userId
            
            if userId is not None:
                MySession.createSession(request, 'userId', userId)
                alert = "Loading.."
                result = True
                MySession.createSession(request, 'email', email)
                send = [result, alert]
                return send
            
            result = False
            alert = "Email and password could not match"
            send = [result, alert]
            return send

    def Profile(request):
        details = UserDetail.objects.get(email = request.session['userId']) 
        return details