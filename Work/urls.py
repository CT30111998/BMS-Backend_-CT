from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(
        constant.EMPLOYEE_REPORT_URLS['attend'],
        views.Attendance.as_view(),
        name=constant.EMPLOYEE_REPORT_VIEWS_NAME['attend']),
    path(
        constant.EMPLOYEE_REPORT_URLS['all_attend'],
        views.AllAttendance.as_view(),
        name=constant.EMPLOYEE_REPORT_VIEWS_NAME['all_attend']),

    path(
        constant.EMPLOYEE_REPORT_URLS['category'],
        views.Category.as_view(),
        name=constant.EMPLOYEE_REPORT_VIEWS_NAME['category'],
    ),
]
