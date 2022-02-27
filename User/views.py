from django.shortcuts import render
# Create your views here.

def homeView(request):
    return render(request, 'index.html')


def loginView(request):
    return render(request, 'user/login.html')


def signUpView(request):
    return render(request, 'user/signup.html')