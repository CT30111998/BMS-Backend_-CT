from django.urls import path
from BMSystem import constants
from . import views

urlpatterns = [
    path(constants.BLOG_URLS['BLOG'], views.BlogMaster.as_view({'get': 'list'})),
    path(constants.BLOG_URLS['GET_BLOG'], views.BlogMaster.as_view({'get': 'retrieve'})),
    path(constants.BLOG_URLS['LIKE'], views.LikBlog.as_view()),
    path(constants.BLOG_URLS['COMMENT'], views.CommentBlog.as_view()),
    # path(constants.BLOG_URLS['UPLOAD'], views.upload_file),
]
