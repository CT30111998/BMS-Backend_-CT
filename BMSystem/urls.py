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


from django.contrib import admin
from django.urls import path, include
from . import constants
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from User import views

urlpatterns = [
    path(constant.USER_URLS['admin'], admin.site.urls, name=constant.USER_VIEWS_NAME['admin']),
    path(constant.DASHBOARD_URL, views.home_view, name=constant.DASHBOARD_VIEW),

    path(constant.USER_URLS['user'], include('User.urls')),
    path(constant.BLOG_URLS['blog'], include('Blog.urls')),
    path(constant.EMPLOYEE_REPORT_URLS['me'], include('Work.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
