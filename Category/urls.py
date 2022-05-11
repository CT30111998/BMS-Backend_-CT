from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [

    path(
        constants.EMPLOYEE_REPORT_URLS['CATEGORY'],
        views.Category.as_view(),
    ),
]
