<<<<<<< HEAD:DjangoAPI/User/urls.py
from . import views
from django.urls import path
from BMSystem import constant

urlpatterns = [
    path(constant.USER_URLS['register'], views.signup, name=constant.USER_VIEWS_NAME['register']),
    path(constant.USER_URLS['login'], views.login, name=constant.USER_VIEWS_NAME['login']),
    path(constant.USER_URLS['logout'], views.logout, name=constant.USER_VIEWS_NAME['logout']),
    path(constant.USER_URLS['profile'], views.profile, name=constant.USER_VIEWS_NAME['profile']),
]
=======
from . import views
from django.urls import path
from BMSystem import constant
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(constant.USER_URLS['register'], views.SignupUser.as_view(), name=constant.USER_VIEWS_NAME['register']),
    path(constant.USER_URLS['login'], views.LoginUser.as_view(), name=constant.USER_VIEWS_NAME['login']),
    path(constant.USER_URLS['logout'], views.logout, name=constant.USER_VIEWS_NAME['logout']),
    path(constant.USER_URLS['profile'], views.ProfileUser.as_view(), name=constant.USER_VIEWS_NAME['profile']),
]

urlpatterns = format_suffix_patterns(urlpatterns)
>>>>>>> development:User/urls.py
