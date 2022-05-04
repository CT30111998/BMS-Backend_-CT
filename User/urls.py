from . import views
from django.urls import path
from BMSystem import constants
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(constants.USER_URLS['register'], views.SignupUser.as_view(), name=constants.USER_VIEWS_NAME['register']),
    path(constants.USER_URLS['login'], views.LoginUser.as_view(), name=constants.USER_VIEWS_NAME['login']),
    path(constants.USER_URLS['logout'], views.Logout.as_view(), name=constants.USER_VIEWS_NAME['logout']),
    path(constants.USER_URLS['profile'], views.ProfileUser.as_view(), name=constants.USER_VIEWS_NAME['profile']),
    path(constants.USER_URLS['get_all'], views.User.as_view(), name=constants.USER_VIEWS_NAME['get_all']),
]

urlpatterns = format_suffix_patterns(urlpatterns)
