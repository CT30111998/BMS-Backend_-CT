"""BMSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from asyncio import constants
from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import constant
from Blog import views as blogView
from Work import views as workView
from User import views as userView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # User Urls
    path(constant.USER_URLS['admin'], admin.site.urls, name=constant.USER_VIEWS_NAME['admin']),
    path(constant.USER_URLS["dashboard"], userView.homeView, name=constant.USER_VIEWS_NAME['dashboard']),
    path(constant.USER_URLS['login'], userView.login, name = constant.USER_VIEWS_NAME['login']),
    # path('login/post', userView.login, name = 'login'),
    path(constant.USER_URLS['register'], userView.signup, name = constant.USER_VIEWS_NAME['register']),
    # path('signup/post', userView.signup, name = 'signup'),
    path('profile/', userView.Profile, name = 'profile'),
    path(constant.USER_URLS['logout'], userView.logout, name = constant.USER_VIEWS_NAME['logout']),
    path('profile/upload', userView.uploadProfile, name = 'uploadProfile'),
    path('uploading/', userView.uploading, name = 'uploading'),
    # end User Urls

    # Employee Report
    path(constant.EMPLOYEE_REPORT_URLS['dashboard'], workView.Me, name=constant.EMPLOYEE_REPORT_VIEWS_NAME['dashboard']),
    # End Employee Report
    
    path(constant.BLOG_URLS['dashboard'], blogView.blog, name=constant.BLOG_VIEWS_NAME['dashboard']),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
