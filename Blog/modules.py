# Blog Modules
from django.core.files.storage import FileSystemStorage
from .models import *
from math import ceil
from django.contrib.auth.models import User as AuthUser
from User.models import *
from django.shortcuts import render
from BMSystem import constant
from BMSystem.base_function import *
from .blog_serializer import *
from json import loads


def get_all_blog(request=None):
    if not request:
        create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if user_id:
        # try:
        get_blogs = Master.objects.filter(deleted=0)
        total_blogs = len(get_blogs)
        total_blog_details = []
        for blog in get_blogs:
            blog_details = {}

            get_user_filter = {
                constant.USER_MODEL_FIELDS['user']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_created_by'])
            }
            get_user = UserMaster.objects.get(**get_user_filter)
            get_user_id = getattr(get_user, constant.USER_MODEL_FIELDS['id'])
            user_name = get_name_from_master_user(get_user)

            blog_details['blog_id'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_id'])
            blog_details['blog_image'] = str(getattr(blog, constant.BLOG_MODEL_FIELDS['blog_image']))
            blog_details['blog_title'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_title'])
            blog_details['blog_desc'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_desc'])
            blog_details['blog_created_by'] = {'id': get_user_id, 'name': user_name}
            blog_details['blog_modify_at'] = getattr(blog, constant.BLOG_MODEL_FIELDS['blog_modify_at'])

            get_like_data_filter = {
                constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_id']),
                constant.BLOG_MODEL_FIELDS['like']: constant.LIKE
            }
            get_likes_data = Like.objects.filter(**get_like_data_filter)
            blog_details['total_like_count'] = len(get_likes_data)

            user_like_details = []
            for get_total_like in get_likes_data:
                user_id = getattr(get_total_like, constant.BLOG_MODEL_FIELDS['like_by'])
                auth_id = AuthUser.objects.get(
                    email=user_id
                )
                get_user = UserMaster.objects.get(user=user_id)
                user_name = get_name_from_master_user(get_user)
                user_detail_dict = {'id': getattr(auth_id, constant.USER_MODEL_FIELDS['id']), 'name': user_name}
                user_like_details.append(user_detail_dict)

            blog_details['total_user_like'] = user_like_details
            like_filter = {
                constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS["blog_id"]),
                constant.BLOG_MODEL_FIELDS['like_by']: get_session(
                    request=request,
                    key=constant.SESSION_USER_ID)}
            try:
                current_user_like_status = Like.objects.filter(**like_filter)[:1].get()
                blog_details['current_user_like_status'] = getattr(
                    current_user_like_status,
                    constant.BLOG_MODEL_FIELDS['like']
                )
            except:
                blog_details['current_user_like_status'] = 0

            get_comment_data_filter = {
                constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_id']),
            }
            get_comment_data = Comment.objects.filter(**get_comment_data_filter)
            blog_details['total_comment'] = len(get_comment_data)
            user_details = []
            for comment in get_comment_data:
                user_id = getattr(comment, constant.BLOG_MODEL_FIELDS["comment_by"])
                auth_id = AuthUser.objects.get(
                    email=user_id
                )
                get_user = UserMaster.objects.filter(**{constant.USER_MODEL_FIELDS['user']: auth_id})[:1].get()
                user_name = get_name_from_master_user(get_user)

                user_comment = getattr(
                    comment,
                    constant.BLOG_MODEL_FIELDS['comment']
                )
                user_detail_dict = {'id': auth_id.id, 'name': user_name, 'comment': user_comment}
                user_details.append(user_detail_dict)
            blog_details['total_user_comment'] = user_details
            total_blog_details.append(blog_details)

        blog_serializer = BlogMasterSerializer(get_blogs, many=True)
        n = len(get_blogs)
        nSlid = n // 4 + ceil((n / 4) - (n // 4))
        alert = constant.GET_ALL_BLOG_DATA_SUCCESSFUL
        params = {'no_of_slides': nSlid, 'total blogs': total_blogs, 'blogs_detail': total_blog_details}
        return create_response(alert=alert, result=True, data=params)
    return create_response(alert=constant.USER_NOT_LOGGED_IN, result=False)


def create_blog(request=None):
    if not request:
        create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if user_id:
        if not request.body:
            alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
            return create_response(result=False, alert=alert)
        get_json_data = loads(request.body)
        if not constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data and \
                not constant.BLOG_MODEL_FIELDS['blog_image'] in get_json_data:
            alert = f"{constant.ONE_FIELD_REQUIRED_FROM_FIELDS} {constant.BLOG_MODEL_FIELDS['blog_title']}" + \
                    f" and {constant.BLOG_MODEL_FIELDS['blog_image']}!"
            return create_response(result=False, alert=alert)
        get_user_details = AuthUser.objects.get(id=user_id)
        blog_params = {constant.BLOG_MODEL_FIELDS['blog_created_by']: get_user_details}

        if constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data:
            blog_params[constant.BLOG_MODEL_FIELDS['blog_title']] = \
                get_json_data[constant.BLOG_MODEL_FIELDS['blog_title']].title()

        if constant.BLOG_MODEL_FIELDS['blog_desc'] in get_json_data:
            blog_params[constant.BLOG_MODEL_FIELDS['blog_desc']] = \
                get_json_data[constant.BLOG_MODEL_FIELDS['blog_desc']].capitalize()

        if constant.BLOG_MODEL_FIELDS['blog_image'] in get_json_data:
            get_file = request.FILES()
            fs = FileSystemStorage()
            path = f"{constant.UPLOAD_PATH}{constant.BLOG_PATH}{get_file.name}"
            fs.save(name=path, content=get_file)
            blog_params[constant.BLOG_MODEL_FIELDS['blog_image']] = path
        try:
            create_new_blog = Master(**blog_params)
            create_new_blog.save()
            return create_response(result=True, alert=constant.CREATE_BLOG_SUCCESSFUL)
        except:
            return create_response(result=False, alert=constant.DATABASE_SERVER_ERROR)

    return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)


def update_blog(request=None):
    if request is None:
        create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)
    get_json_data = loads(request.body)

    if not constant.BLOG_MODEL_FIELDS['get_blog_id'] in get_json_data:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)

    if not constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data and \
            not constant.BLOG_MODEL_FIELDS['blog_desc'] in get_json_data:
        alert = f"{constant.ONE_FIELD_REQUIRED_FROM_FIELDS} {constant.BLOG_MODEL_FIELDS['blog_title']}" + \
                f" and {constant.BLOG_MODEL_FIELDS['blog_desc']}!"
        return create_response(result=False, alert=alert)

    blog_id = get_json_data['blog_id']
    blog_filter = {constant.BLOG_MODEL_FIELDS['blog_id']: blog_id}
    get_blog = Master.objects.filter(**blog_filter)
    if not get_blog:
        return create_response(result=False, alert=constant.BLOG_NOT_EXIST)

    blog_params = {}
    if constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data:
        blog_params[constant.BLOG_MODEL_FIELDS['blog_title']] = \
            get_json_data[constant.BLOG_MODEL_FIELDS['blog_title']].title()
    if constant.BLOG_MODEL_FIELDS['blog_desc'] in get_json_data:
        blog_params[constant.BLOG_MODEL_FIELDS['blog_desc']] = \
            get_json_data[constant.BLOG_MODEL_FIELDS['blog_desc']].capitalize()
    try:
        get_blog.update(**blog_params)
    except:
        return create_response(result=False, alert=constant.UPDATE_FAIL)
    return create_response(result=True, alert=constant.BLOG_UPDATE_SUCCESSFUL)


def delete_blog(request):
    if not request or not request.body:
        create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)
    try:
        get_json_data = loads(request.body)
    except:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)

    if not constant.BLOG_MODEL_FIELDS['get_blog_id'] in get_json_data:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)

    blog_id = get_json_data[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    blog_filter = {
        constant.BLOG_MODEL_FIELDS['blog_id']: blog_id,
        constant.BLOG_MODEL_FIELDS['blog_delete']: constant.BLOG_NOT_DELETE_NUM,
        constant.BLOG_MODEL_FIELDS['blog_created_by']: user_id
    }
    get_blog = Master.objects.filter(**blog_filter)
    if not get_blog:
        return create_response(result=False, alert=constant.BLOG_NOT_EXIST)
    try:
        # get_blog.update(**{constant.BLOG_MODEL_FIELDS['blog_delete']: constant.BLOG_DELETE_NUM})
        get_blog.delete()
    except:
        return create_response(result=False, alert=constant.BLOG_NOT_DELETE)

    return create_response(result=True, alert=constant.BLOG_DELETE_SUCCESSFUL)


def like_blog(request=None):
    if not request:
        create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)

    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)
    get_json_response = loads(request.body)

    if constant.BLOG_MODEL_FIELDS['get_blog_id'] and constant.BLOG_MODEL_FIELDS['like_status'] not in get_json_response:
        alert = get_payload_error_alert(
            constant.BLOG_MODEL_FIELDS['get_blog_id'],
            constant.BLOG_MODEL_FIELDS['like_status']
        )
        return create_response(result=False, alert=alert)

    blog_id = get_json_response[constant.BLOG_MODEL_FIELDS['get_blog_id']]

    get_like_status = get_json_response[constant.BLOG_MODEL_FIELDS['like_status']] \
        if constant.BLOG_MODEL_FIELDS['like_status'] in get_json_response else 0
    like_filter = {
        constant.BLOG_MODEL_FIELDS['blog']: blog_id,
        constant.BLOG_MODEL_FIELDS['like_by']: user_id
    }
    alert = constant.BLOG_LIKE_SUCCESSFUL
    if get_like_status == 0:
        alert = constant.BLOG_UNLIKE_SUCCESSFUL
    get_like_blog = Like.objects.filter(**like_filter)
    like_params = {constant.BLOG_MODEL_FIELDS['like']: get_like_status}
    if get_like_blog:
        get_like_blog.update(**like_params)
    else:
        get_user = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: user_id})
        try:
            get_blog = Master.objects.get(**{constant.BLOG_MODEL_FIELDS['blog_id']: blog_id})
        except:
            return create_response(result=False, alert=constant.BLOG_NOT_EXIST)
        like_params[constant.BLOG_MODEL_FIELDS['like_by']] = get_user
        like_params[constant.BLOG_MODEL_FIELDS['blog']] = get_blog
        like_blog = Like(**like_params)
        like_blog.save()

    return create_response(result=True, alert=alert)


def comment_blog(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)

    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)
    get_json_response = loads(request.body)
    if constant.BLOG_MODEL_FIELDS['get_blog_id'] not in get_json_response \
            or constant.BLOG_MODEL_FIELDS['comment'] not in get_json_response:
        alert = get_payload_error_alert(
            constant.BLOG_MODEL_FIELDS['get_blog_id'], constant.BLOG_MODEL_FIELDS['comment']
        )
        return create_response(result=False, alert=alert)

    blog_id = get_json_response[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    comment = get_json_response[constant.BLOG_MODEL_FIELDS['comment']].capitalize()

    comment_filter = {
        constant.BLOG_MODEL_FIELDS['comment_by']: user_id,
        constant.BLOG_MODEL_FIELDS['blog']: blog_id
    }
    blog_comment = Comment.objects.filter(**comment_filter)
    if not blog_comment:
        try:
            get_blog = Master.objects.get(**{constant.BLOG_MODEL_FIELDS['blog_id']: blog_id})
        except:
            return create_response(result=False, alert=constant.BLOG_NOT_EXIST)
        get_user = AuthUser.objects.filter(**{constant.USER_MODEL_FIELDS['id']: user_id})[:1].get()
        comment_params = {
            constant.BLOG_MODEL_FIELDS['blog']: get_blog,
            constant.BLOG_MODEL_FIELDS['comment_by']: get_user,
            constant.BLOG_MODEL_FIELDS['comment']: comment
        }
        comment_object = Comment(**comment_params)
        comment_object.save()
        alert = constant.CREATE_COMMENT_SUCCESSFUL
    else:
        comment_params = {
            constant.BLOG_MODEL_FIELDS['comment']: comment
        }
        blog_comment.update(**comment_params)
        alert = constant.UPDATE_COMMENT_SUCCESSFUL
    return create_response(result=True, alert=alert)


def delete_comment_blog(request=None):
    if not request:
        return create_response(result=False, alert=constant.UNEXPECTED_ERROR)
    user_id = get_session(request=request, key=constant.SESSION_USER_ID)
    if not user_id:
        return create_response(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)

    get_json_response = loads(request.body)
    if constant.BLOG_MODEL_FIELDS['get_blog_id'] not in get_json_response:
        alert = get_payload_error_alert(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return create_response(result=False, alert=alert)

    blog_id = get_json_response[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    comment_filter = {
        constant.BLOG_MODEL_FIELDS['comment_by']: user_id,
        constant.BLOG_MODEL_FIELDS['blog']: blog_id
    }
    get_comment = Comment.objects.filter(**comment_filter)
    if not get_comment:
        return create_response(result=False, alert=constant.COMMENT_NOT_EXIST)
    get_comment.delete()
    return create_response(result=True, alert=constant.DELETE_COMMENT_SUCCESSFUL)
