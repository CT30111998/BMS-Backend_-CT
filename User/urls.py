from . import views
from django.urls import path
from BMSystem import constant
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(constant.USER_URLS['register'], views.SignupUser.as_view(), name=constant.USER_VIEWS_NAME['register']),
    path(constant.USER_URLS['login'], views.LoginUser.as_view(), name=constant.USER_VIEWS_NAME['login']),
    path(constant.USER_URLS['logout'], views.Logout.as_view(), name=constant.USER_VIEWS_NAME['logout']),
    path(constant.USER_URLS['profile'], views.ProfileUser.as_view(), name=constant.USER_VIEWS_NAME['profile']),
]

urlpatterns = format_suffix_patterns(urlpatterns)
