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
    user_id = get_session(request=request, key='userId')
    if user_id:
        # try:
        get_blogs = Master.objects.all()
        total_blog_details = []
        for blog in get_blogs:
            blog_details = {}
            user_details = []
            get_user = UserMaster.objects.get(user=blog.created_by)
            user_name = f"\
                                            {getattr(get_user, constant.USER_MODEL_FIELDS['first_name'])} \
                                            {getattr(get_user, constant.USER_MODEL_FIELDS['last_name'])}"

            blog_details['blog_image'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_image'])
            blog_details['blog_title'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_title'])
            blog_details['blog_desc'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_desc'])
            blog_details['blog_created_by'] = {'id': user_id, 'name': user_name}
            blog_details['blog_modify_at'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_modify_at'])

            get_likes_data = Like.objects.filter(blog=blog.id, like=constant.LIKE)
            blog_details['total_like_count'] = len(get_likes_data)
            for get_total_like in get_likes_data:
                user_id = get_total_like.user
                get_user = UserMaster.objects.get(user=user_id)
                user_name = f"\
                        {getattr(get_user, constant.USER_MODEL_FIELDS['first_name'])} \
                        {getattr(get_user, constant.USER_MODEL_FIELDS['last_name'])}"
                user_detail_dict = {'id': user_id, 'name': user_name}
                user_details.append(user_detail_dict)
            blog_details['total_user_like'] = user_details
            user_details.clear()

            current_user_like_status = Like.objects.get(
                blog=blog.id,
                user=get_session(
                    request=request,
                    key=constant.SESSION_USER_ID))
            blog_details['current_user_like_status'] = getattr(current_user_like_status,
                                                               constant.BLOG_MODEL_FIELDS['like']) \
                if current_user_like_status else constant.UNLIKE

            get_comment_data = Comment.objects.filter(blog=blog.id)
            blog_details['total_comment'] = len(get_comment_data)
            for user_blog_details in blog_details:
                user_id = user_blog_details.user
                get_user = UserMaster.objects.get(user=user_id)
                user_name = f"\
                                        {getattr(get_user, constant.USER_MODEL_FIELDS['first_name'])} \
                                        {getattr(get_user, constant.USER_MODEL_FIELDS['last_name'])}"
                user_comment = getattr(
                    user_blog_details,
                    constant.BLOG_MODEL_FIELDS['comment']
                )
                user_detail_dict = {'id': user_id, 'name': user_name, 'comment': user_comment}
                user_details.append(user_detail_dict)
            blog_details['total_user_like'] = user_details
            total_blog_details.append(blog_details)
            user_details.clear()

        blog_serializer = BlogMasterSerializer(get_blogs, many=True)
        n = len(get_blogs)
        nSlid = n // 4 + ceil((n / 4) - (n // 4))
        result = True
        alert = constant.GET_ALL_BLOG_DATA_SUCCESSFUL
        params = {'no_of_slides': nSlid, 'blogs_detail': total_blog_details}
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
