from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(constants.BLOG_URLS['dashboard'], views.BlogMaster.as_view()),
    # path(constant.BLOG_URLS['blog_update'], views.UpdateBlog.as_view()),
    path(constants.BLOG_URLS['blog_like'], views.LikBlog.as_view()),
    path(constants.BLOG_URLS['blog_comment'], views.CommentBlog.as_view(),
         name=constants.BLOG_VIEWS_NAME['blog_comment']),
    path(constants.BLOG_URLS['upload'], views.upload_file),
]
