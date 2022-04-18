from django.urls import path
from BMSystem import constant
from . import views

urlpatterns = [
    path(constant.BLOG_URLS['dashboard'], views.BlogMaster.as_view(), name=constant.BLOG_VIEWS_NAME['dashboard']),
    # path(constant.BLOG_URLS['blog_update'], views.UpdateBlog.as_view(), name=constant.BLOG_VIEWS_NAME['blog_update']),
    path(constant.BLOG_URLS['blog_like'], views.LikBlog.as_view(), name=constant.BLOG_VIEWS_NAME['blog_like']),
    path(constant.BLOG_URLS['blog_comment'], views.CommentBlog.as_view(),
         name=constant.BLOG_VIEWS_NAME['blog_comment']),
]
