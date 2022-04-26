from django.shortcuts import redirect, render
from .moduals.authModels import *
from BMSystem import constant
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from BMSystem.base_function import create_response, check_response_result, check_user_loging
from rest_framework.permissions import IsAuthenticated
import json


def home_view(request):
    return render(request, 'index.html')


class User(APIView):
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = get_all_user_data(request)
        return get_response

    def delete(self, request):
        get_response = delete_user(request)
        return get_response


class SignupUser(APIView):
    # @api_view([constant.GET])
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        return render(request, constant.USER_TEMPLATE_DIR + constant.USER_TEMPLATES['register'])

    # @api_view([constant.POST])
    def post(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if user_id:
            return create_response(result=False, alert=constant.USER_LOGGED_IN)
        get_api_response = create_my_user(request)
        return get_api_response


class LoginUser(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get(self, request, format=None):
    #     return render(request, constant.USER_TEMPLATE_DIR + constant.USER_TEMPLATES['login'])

    def post(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if user_id:
            return create_response(result=False, alert=constant.USER_LOGGED_IN)
        get_api_response = user_login(request)
        return get_api_response


class ProfileUser(APIView):
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_api_response = user_profile(request, user_id)
        return get_api_response

    def put(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_api_response = update_profile(request, user_id)
        return get_api_response


# @api_view([constant.GET])
class Logout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
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
