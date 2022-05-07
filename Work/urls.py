from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(
        constants.EMPLOYEE_REPORT_URLS['attend'],
        views.Attendance.as_view(),
        name=constants.EMPLOYEE_REPORT_VIEWS_NAME['attend']),
    path(
        constants.EMPLOYEE_REPORT_URLS['all_attend'],
        views.AllAttendance.as_view(),
        name=constants.EMPLOYEE_REPORT_VIEWS_NAME['all_attend']),

    path(
        constants.EMPLOYEE_REPORT_URLS['category'],
        views.Category.as_view(),
        name=constants.EMPLOYEE_REPORT_VIEWS_NAME['category'],
    ),
    path(
        constants.EMPLOYEE_REPORT_URLS['feedback'],
        views.Feedback.as_view({'get': 'list'}),
    ),
]
