from django.shortcuts import redirect, render
from .moduals.authModels import get_all_user_data, delete_user, update_profile, user_profile
from BMSystem import constants, response_messages
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from BMSystem.base_function import check_response_result, check_user_loging
from base.common_helpers import create_response


class User(APIView):
    def get(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_all_user_data(request)
        return get_response

    def delete(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = delete_user(request, get_user_id=user_id)
        return get_response


class ProfileUser(APIView):
    def get(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_api_response = user_profile(request, user_id)
        return get_api_response

    def put(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_api_response = update_profile(request, user_id)
        return get_api_response
