from django.shortcuts import render
from rest_framework.views import APIView
from Work.modules import (
    get_all_user_attendance, get_user_attendance, create_user_attendance, delete_user_attendance, get_all_cat,
    create_category
)
from BMSystem.base_function import check_user_loging, check_response_result, create_response


# Create your views here.


def Me(request):
    return render(request, "work/index.html")


class Attendance(APIView):
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = get_user_attendance(request, user_id)
        return get_response

    def post(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = create_user_attendance(request, user_id)
        return get_response

    def put(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = create_user_attendance(request, user_id)
        return get_response

    def delete(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = delete_user_attendance(request, user_id)
        return get_response


class AllAttendance(APIView):
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = get_all_user_attendance(request, user_id)
        return get_response


class Category(APIView):
    def get(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = get_all_cat(request, user_id)
        return get_response

    def post(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = create_category(request, user_id)
        return get_response

    def put(self, request):
        response = check_user_loging(request)
        user_id = check_response_result(response)
        if not user_id:
            return create_response(response)
        get_response = create_category(request, user_id)
        return get_response
