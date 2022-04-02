from re import template
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .moduals.authModels import authUser
from .models import User as UserDetail
from django.contrib import auth
from BMSystem import constant
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
# Create your views here.


def homeView(request):
    return render(request, 'index.html')


@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        login = authUser()
        get_api_response = login.Login(request)
        return Response(get_api_response)
    return render(request, constant.USER_TEMPLATE_DIR+constant.USER_TEMPLATES['login'])


@api_view(['POST', 'GET'])
def signup(request):
    if request.method == "POST":
        createUser = authUser()
        get_api_response = createUser.createMyUser(request)
        return Response(get_api_response)
    return render(request, constant.USER_TEMPLATE_DIR+constant.USER_TEMPLATES['register'])


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


