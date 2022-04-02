from re import template
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .moduals.authModels import authUser
from .models import User as UserDetail
from django.contrib import auth
# Create your views here.

def homeView(request):
    return render(request, 'index.html')


def login(request):
    login = authUser()
    result = login.Login(request)
    if result[0]:
        return redirect('/')
    return render(request, 'user/login.html', {"alert":result[1]})



def signup(request):
    if request.method == "POST":
        createUser = authUser()
        alert, result, template = createUser.createMyUser(template)
        return render(request, template, {"result": alert})
    login = authUser()
    template = login.createMyUser(request)
    return render(request, template)


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


