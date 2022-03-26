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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from Blog import views as blogView
from Work import views as workView
from User import views as userView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', userView.homeView, name='home'),
    path('me/', workView.Me, name='me'),
    path('login/', userView.loginView, name = 'loginView'),
    path('login/post', userView.login, name = 'login'),
    path('signup/', userView.signUpView, name = 'signupView'),
    path('signup/post', userView.signup, name = 'signup'),

    path('profile/', userView.Profile, name = 'profile'),
    path('logout/', userView.logout, name = 'logout'),
    path('profile/upload', userView.uploadProfile, name = 'uploadProfile'),
    path('uploading/', userView.uploading, name = 'uploading'),
    path('blog/', blogView.blog, name="blog"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
