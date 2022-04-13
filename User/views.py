from django.shortcuts import redirect, render
from .moduals.authModels import *
from BMSystem import constant
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    return render(request, 'index.html')


class SignupUser(APIView):
    # @api_view([constant.GET])
    def get(self, request, format=None):
        return render(request, constant.USER_TEMPLATE_DIR + constant.USER_TEMPLATES['register'])

    # @api_view([constant.POST])
    def post(self, request, format=None):
        get_api_response = create_my_user(request)
        return get_api_response


class LoginUser(APIView):
    def get(self, request, format=None):
        return render(request, constant.USER_TEMPLATE_DIR + constant.USER_TEMPLATES['login'])

    def post(self, request, format=None):
        get_api_response = user_login(request)
        print("API RESPONSE = ", get_api_response)
        return get_api_response


class ProfileUser(APIView):
    def get(self, request, user_id):
        get_api_response = user_profile(request, user_id)
        return get_api_response


@api_view([constant.GET])
def logout(request):
    get_api_response = user_logout(request)
    return get_api_response


# @api_view([constant.POST])
# def login(request, format=None):
#     get_api_response = user_login(request)
#     print("API RESPONSE = ", get_api_response)
#     return get_api_response
# @api_view([constant.POST, constant.PUT, constant.GET])
# def profile(request, user_id):
#     get_api_response = user_profile(request, user_id)
#     return get_api_response
