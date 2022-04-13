# Blog Modules
from .models import *
from math import ceil
from django.contrib.auth.models import User as AuthUser
from User.models import *
from django.shortcuts import render
from BMSystem import constant
from BMSystem.base_function import *
from .blog_serializer import *


def get_all_blog(request):
    user = get_session(request=request, key='userId')
    if user:
        # try:
        get_blogs = Blog.objects.all()
        total_blog_details = []
        for blog in get_blogs:
            blog_details = {}
            get_total_likes = Like.objects.filter(blog=blog.id, like=constant.LIKE)
            for get_total_like in get_total_likes:
                user_id = get_total_like.user
                user = UserMaster.objects.get(user=user_id)

            current_like = Like.objects.get(
                blog=blog.id,
                user=get_session(
                    request=request,
                    key=constant.SESSION_USER_ID)).like

            comments = Comment.objects.filter(blog=blog.id)

        blog_serializer = BlogMasterSerializer(blogs, many=True)
        n = len(blogs)
        nSlid = n // 4 + ceil((n / 4) - (n // 4))
        result = True
        alert = constant.GET_ALL_BLOG_DATA_SUCCESSFUL
        params = {'no_of_slides': nSlid, 'blog': blog_serializer.data}
        return create_response(alert=alert, result=result, data=params)
        # except:
        #     result = False
        #     alert = constant.GET_ALL_BLOG_DATA_FAIL
        #     return create_response(alert=alert, result=result)
    result = False
    alert = constant.USER_NOT_LOGGED_IN
    return create_response(alert=alert, result=result)


def create_blog(request):
    pass

