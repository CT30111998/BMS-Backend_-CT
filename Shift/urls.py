from .views import Department
from django.urls import path
from BMSystem import constants

urlpatterns = [
    path(constants.USER_URLS['SHIFT'], Department.as_view()),
    # path(constants.USER_URLS['USER_DEPARTMENT'], UserDepartment.as_view()),
]
