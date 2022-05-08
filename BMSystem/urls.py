"""
    BMSystem URL Configuration
"""


from django.contrib import admin
from django.urls import path, include
from . import constants
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from User import views

urlpatterns = [
    path(constants.AUTH_URLS['ADMIN'], admin.site.urls),

    path(constants.URLS_PATH['AUTH'], include('Auth.urls')),
    path(constants.URLS_PATH['USERS'], include('User.urls')),
    path(constants.URLS_PATH['BLOG'], include('Blog.urls')),
    path(constants.URLS_PATH['WORK'], include('Work.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
