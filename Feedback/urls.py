from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [

    path(
        constants.EMPLOYEE_REPORT_URLS['FEEDBACK'],
        views.Feedback.as_view({'get': 'list'}),
    ),
]
