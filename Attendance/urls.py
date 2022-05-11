from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(
        constants.EMPLOYEE_REPORT_URLS['ATTEND'],
        views.Attendance.as_view({'get': 'retrieve'}),
    ),

    path(
        constants.EMPLOYEE_REPORT_URLS['GET_ALL_ATTEND'],
        views.Attendance.as_view({'get': 'list'}),
    ),
]
