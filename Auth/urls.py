from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(
        constants.AUTH_URLS['REGISTER'],
        views.SignUp.as_view(),
    ),

    path(
        constants.AUTH_URLS['LOGIN'],
        views.Login.as_view(),
    ),

    path(
        constants.AUTH_URLS['LOGOUT'],
        views.Logout.as_view(),
    ),
]
