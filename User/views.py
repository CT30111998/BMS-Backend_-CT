from django.shortcuts import redirect, render
from .moduals.authModels import get_all_user_data, delete_user, update_profile, user_profile
from BMSystem import constants, response_messages
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from BMSystem.base_function import check_response_result, get_user_id_from_request
from base.common_helpers import create_response
from Auth.jwt_module import JWTAuthentication


class User(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_all_user_data(request.GET)
        return get_response

    def delete(self, request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = delete_user(user_id=user_id)
        return get_response

    def put(self, request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_api_response = update_profile(request, user_id)
        return get_api_response


class Department(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    def get(self):
        return create_response(result=True)

    def post(self):
        return create_response(result=True)

    def put(self):
        return create_response(result=True)

    def delete(self):
        return create_response(result=True)


class ProfileUser(APIView):
    def get(self, request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_api_response = user_profile(request, user_id)
        return get_api_response


