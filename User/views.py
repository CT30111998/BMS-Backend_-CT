from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .moduals.authModels import authUser
from .models import User as UserDetail
from django.contrib import auth
# Create your views here.

def homeView(request):
    return render(request, 'index.html')


def loginView(request):
    return render(request, 'user/login.html')


def login(request):
    login = authUser()
    result = login.Login(request)
    if result[0]:
        return redirect('/')
    return render(request, 'user/login.html', {"alert":result[1]})


def signUpView(request):
    return render(request, 'user/signup.html')


def signup(request):
    if request.method == "POST":
        signUp = authUser()
        result = signUp.createMyUser(request)
        if result[0]:
            return redirect('/')
    return render(request, 'user/login.html', {"alert":result[1]})


def logout(request):
    auth.logout(request)
    return redirect('/')


def Profile(request):
    auth = User()
    if auth.is_authenticated:
        user = authUser.Profile(request)
        return render(request, 'user/profile.html', {'userData':user})
    return redirect('/')

def uploadProfile(request):
    upload = True
    auth = User()
    if auth.is_authenticated:
        user = authUser.Profile(request)
        return render(request, 'user/profile.html', {'userData':user, 'upload': upload})
    return redirect('/')

def uploading(request):
    upload = authUser()
    name = authUser.updateProfile(request)
    print(name)
    return redirect('/profile/')


