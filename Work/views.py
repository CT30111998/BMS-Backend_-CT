from django.shortcuts import render
from rest_framework.views import APIView
from Work.modules import *
# Create your views here.


def Me(request):
    return render(request, "work/index.html")


class Attendance(APIView):
    def get(self, request):
        get_response = get_user_attendance(request)
        return get_response

    def post(self, request):
        get_response = create_user_attendance(request)
        return get_response

    def put(self, request):
        get_response = create_user_attendance(request)
        return get_response

    def delete(self, request):
        get_response = delete_user_attendance(request)
        return get_response


class AllAttendance(APIView):
    def get(self, request):
        get_response = get_all_user_attendance(request)
        return get_response
