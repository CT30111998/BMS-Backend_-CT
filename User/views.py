from django.shortcuts import redirect, render
from .moduals.authModels import authUser
# Create your views here.

def homeView(request):
    return render(request, 'index.html')


def loginView(request):
    return render(request, 'user/login.html')


def login(request):
    return redirect('/')


def signUpView(request):
    return render(request, 'user/signup.html')


def signup(request):
    if request.method == "POST":
        signUp = authUser()
        result = signUp.createMyUser(request)
        print(result)
    print("hello")
    return redirect('/')


