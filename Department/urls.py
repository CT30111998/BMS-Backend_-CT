from .views import Department
from django.urls import path
from BMSystem import constants

urlpatterns = [
    path(constants.USER_URLS['DEPARTMENT'], Department.as_view()),
    # path(constants.USER_URLS['USER_DEPARTMENT'], UserDepartment.as_view()),
]