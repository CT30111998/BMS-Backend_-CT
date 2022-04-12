# Blog Modules
from models import *
from math import ceil
from django.shortcuts import render
from BMSystem import constant
from BMSystem.base_function import *


def get_all_blog(request):
    user = get_session(request=request, key='userId')
    if user:
        try:
            blogs = Blog.objects.all()
            n = len(blogs)
            nSlid = n // 4 + ceil((n / 4) - (n // 4))
            result = True
            alert = constant.GET_ALL_BLOG_DATA_SUCCESSFUL
            params = {'no_of_slids': nSlid, 'range': range(nSlid), 'blog': blogs}
            return create_response(alert=alert, result=result, data=params)
        except:
            result = False
            alert = constant.GET_ALL_BLOG_DATA_FAIL
            return create_response(alert=alert, result=result)
    result = False
    alert = constant.USER_NOT_LOGGED_IN
    return create_response(alert=alert, result=result)


def create_blog(request):
    pass

