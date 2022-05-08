from . import views
from django.urls import path
from BMSystem import constants
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(constants.USER_URLS['PROFILE'], views.ProfileUser.as_view()),
    path(constants.USER_URLS['GET_ALL'], views.User.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
