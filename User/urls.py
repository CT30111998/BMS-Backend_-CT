from . import views
from django.urls import path
from BMSystem import constant

urlpatterns = [
    path(constant.USER_URLS['register'], views.signup, name=constant.USER_VIEWS_NAME['register']),
    path(constant.USER_URLS['login'], views.login, name=constant.USER_VIEWS_NAME['login']),
    path(constant.USER_URLS['logout'], views.logout, name=constant.USER_VIEWS_NAME['logout']),
    path(constant.USER_URLS['profile'], views.profile, name=constant.USER_VIEWS_NAME['profile']),
]
