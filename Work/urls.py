from django.urls import path
from BMSystem import constant
from . import views

urlpatterns = [
    path(constant.EMPLOYEE_REPORT_URLS['me'], views.Me,
         name=constant.EMPLOYEE_REPORT_VIEWS_NAME['dashboard']),
]