from django.shortcuts import redirect, render
from .moduals.authModels import authUser
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
    logout(request)
    return redirect('/')

def Profile(request):
    get = authUser()
    user = get.Profile(request)
    return render(request, 'user/profile.html', {'user':user})


