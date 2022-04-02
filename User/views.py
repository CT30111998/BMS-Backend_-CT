from django.shortcuts import redirect, render
from .moduals.authModels import *
from BMSystem import constant
from rest_framework.decorators import api_view


def home_view(request):
    return render(request, 'index.html')


@api_view([constant.POST, constant.GET])
def login(request):
    if request.method == constant.POST:
        get_api_response = user_login(request)
        return get_api_response
    return render(request, constant.USER_TEMPLATE_DIR+constant.USER_TEMPLATES['login'])


@api_view([constant.POST, constant.GET])
def signup(request):
    if request.method == constant.POST:
        get_api_response = create_my_user(request)
        return get_api_response
    return render(request, constant.USER_TEMPLATE_DIR+constant.USER_TEMPLATES['register'])


@api_view([constant.GET])
def logout(request):
    get_api_response = user_logout(request)
    return get_api_response


@api_view([constant.POST, constant.PUT, constant.GET])
def profile(request, user_id):
    get_api_response = user_profile(request, user_id)
    return get_api_response



