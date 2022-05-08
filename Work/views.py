from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from Work.modules import (
    get_all_user_attendance, get_user_attendance, create_user_attendance, delete_user_attendance, get_all_cat,
    create_category, get_feedback, create_feedback, update_feedback, delete_feedback
)
from BMSystem.base_function import check_user_loging, check_response_result
from base.common_helpers import create_response
from BMSystem import constants, response_messages

# Create your views here.


class Attendance(APIView):
    def get(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_user_attendance(request, user_id)
        return get_response

    def post(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = create_user_attendance(request, user_id)
        return get_response

    def put(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = create_user_attendance(request, user_id)
        return get_response

    def delete(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = delete_user_attendance(request, user_id)
        return get_response


class AllAttendance(APIView):
    def get(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_all_user_attendance(request, user_id)
        return get_response


class Category(APIView):

    def get(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_all_cat(request, user_id)
        return get_response

    def post(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = create_category(request, user_id)
        return get_response

    def put(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = create_category(request, user_id)
        return get_response


class Feedback(ViewSet):

    def list(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = get_feedback(request)
        return get_response

    def retrieve(self, request):
        pass

    def post(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = create_feedback(request, user_id=user_id)
        return get_response

    def put(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = update_feedback(request)
        return get_response

    def delete(self, request):
        user_id = check_user_loging(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = delete_feedback(request, user_id=user_id)
        return get_response
