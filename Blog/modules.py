# Blog Modules
from .models import *
from math import ceil
from django.contrib.auth.models import User as AuthUser
from User.models import *
from django.shortcuts import render
from BMSystem import constant
from BMSystem.base_function import *
from .blog_serializer import *
from json import loads


def get_all_blog(request):
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if user_id:
        # try:
        get_blogs = Master.objects.all()
        total_blogs = len(get_blogs)
        total_blog_details = []
        for blog in get_blogs:
            blog_details = {}
            user_details = []
            get_user_filter = {
                constant.USER_MODEL_FIELDS['user']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_created_by'])
            }
            get_user = UserMaster.objects.get(**get_user_filter)
            user_name = f"\
{getattr(get_user, constant.USER_MODEL_FIELDS['first_name'])} \
{getattr(get_user, constant.USER_MODEL_FIELDS['last_name'])}"

            blog_details['blog_image'] = str(getattr(blog, constant.BLOG_MODEL_FIELDS['blog_image']))
            blog_details['blog_title'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_title'])
            blog_details['blog_desc'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_desc'])
            blog_details['blog_created_by'] = {'id': user_id, 'name': user_name}
            blog_details['blog_modify_at'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_modify_at'])

            get_like_data_filter = {
                constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_id']),
                constant.BLOG_MODEL_FIELDS['like']: constant.LIKE
            }
            get_likes_data = Like.objects.filter(**get_like_data_filter)
            blog_details['total_like_count'] = len(get_likes_data)
            for get_total_like in get_likes_data:
                user_id = get_total_like.user
                get_user = UserMaster.objects.get(user=user_id)
                user_name = f"{getattr(get_user, constant.USER_MODEL_FIELDS['first_name'])}\
                        {getattr(get_user, constant.USER_MODEL_FIELDS['last_name'])}"
                user_detail_dict = {'id': user_id, 'name': user_name}
                user_details.append(user_detail_dict)
            blog_details['total_user_like'] = user_details
            user_details.clear()
            like_filter = {
                constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS["blog_id"]),
                constant.BLOG_MODEL_FIELDS['like_by']: get_session(
                    request=request,
                    key=constant.SESSION_USER_ID)}
            current_user_like_status = Like.objects.filter(**like_filter)
            blog_details['current_user_like_status'] = getattr(current_user_like_status,
                                                               constant.BLOG_MODEL_FIELDS['like']) \
                if current_user_like_status else constant.UNLIKE
            get_comment_data = Comment.objects.filter(blog=blog.id)
            blog_details['total_comment'] = len(get_comment_data)
            for user_blog_details in get_comment_data:
                user_id = getattr(user_blog_details, constant.BLOG_MODEL_FIELDS["comment_by"])
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
        params = {'no_of_slides': nSlid, 'total blogs': total_blogs, 'blogs_detail': total_blog_details}
        return create_response(alert=alert, result=result, data=params)
        # except:
        #     result = False
        #     alert = constant.GET_ALL_BLOG_DATA_FAIL
        #     return create_response(alert=alert, result=result)
    result = False
    alert = constant.USER_NOT_LOGGED_IN
    return create_response(alert=alert, result=result)


def create_blog(request):
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if user_id:
        get_json_data = loads(request.body)
        if not constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data and \
                not constant.BLOG_MODEL_FIELDS['blog_image'] in get_json_data:
            alert = f"{constant.ONE_FIELD_REQUIRED_FROM_FIELDS} {constant.BLOG_MODEL_FIELDS['blog_title']} and \
            {constant.BLOG_MODEL_FIELDS['blog_image']}!"
            return create_response(result=False, alert=alert)
        get_user_details = AuthUser.objects.get(id=user_id)
        blog_params = {constant.BLOG_MODEL_FIELDS['blog_created_by']: get_user_details}
        if constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data:
            blog_params[constant.BLOG_MODEL_FIELDS['blog_title']] = \
                get_json_data[constant.BLOG_MODEL_FIELDS['blog_title']]
        if constant.BLOG_MODEL_FIELDS['blog_desc'] in get_json_data:
            blog_params[constant.BLOG_MODEL_FIELDS['blog_desc']] = \
                get_json_data[constant.BLOG_MODEL_FIELDS['blog_desc']]
        if constant.BLOG_MODEL_FIELDS['blog_image'] in get_json_data:
            blog_params[constant.BLOG_MODEL_FIELDS['blog_image']] = \
                get_json_data[constant.BLOG_MODEL_FIELDS['blog_image']]
        try:
            create_new_blog = Master(**blog_params)
            create_new_blog.save()
            return create_response(result=True, alert=constant.CREATE_BLOG_SUCCESSFUL)
        except:
            return create_response(result=False, alert=constant.DATABASE_SERVER_ERROR)

    return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
