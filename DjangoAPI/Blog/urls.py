from django.urls import path
from BMSystem import constant
from . import views

urlpatterns = [
    path(constant.BLOG_URLS['dashboard'], views.blog, name=constant.BLOG_VIEWS_NAME['dashboard']),
]
