# Blog Modules
from django.core.files.storage import FileSystemStorage
from .models import Master as BlogMaster, Like as LikeMaster, Comment as CommentMaster
from math import ceil
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster as MasterUser
from BMSystem import constant
from BMSystem.base_function import \
    create_response as my_response_create, \
    get_session as my_session_get, \
    get_name_from_master_user as my_name_create, \
    get_payload_error_alert as my_payload_error
from .blog_serializer import BlogMasterSerializer as BlogSerializer
from json import loads


def get_all_blog(request=None, get_user_id=None):
    if not request:
        my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(alert=constant.USER_NOT_LOGGED_IN, result=False)

    get_blogs = BlogMaster.objects.filter(**{
        constant.BLOG_MODEL_FIELDS['blog_delete']: constant.BLOG_NOT_DELETE_NUM
    })
    total_blogs = len(get_blogs)
    total_blog_details = []
    for blog in get_blogs:
        blog_details = {}

        get_user_filter = {
            constant.USER_MODEL_FIELDS['user']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_created_by'])
        }
        get_user = MasterUser.objects.get(**get_user_filter)
        get_user_id = getattr(get_user, constant.USER_MODEL_FIELDS['id'])
        user_name = my_name_create(get_user)

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
        get_likes_data = LikeMaster.objects.filter(**get_like_data_filter)
        blog_details['total_like_count'] = len(get_likes_data)

        user_like_details = []
        for get_total_like in get_likes_data:
            user_id = getattr(get_total_like, constant.BLOG_MODEL_FIELDS['like_by'])
            auth_id = AuthUser.objects.get(
                email=user_id
            )
            get_user = MasterUser.objects.get(user=user_id)
            user_name = my_name_create(get_user)
            user_detail_dict = {'id': getattr(auth_id, constant.USER_MODEL_FIELDS['id']), 'name': user_name}
            user_like_details.append(user_detail_dict)

        blog_details['total_user_like'] = user_like_details
        like_filter = {
            constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS["blog_id"]),
            constant.BLOG_MODEL_FIELDS['like_by']: my_session_get(
                request=request,
                key=constant.SESSION_USER_ID)}
        try:
            current_user_like_status = LikeMaster.objects.filter(**like_filter)[:1].get()
            blog_details['current_user_like_status'] = getattr(
                current_user_like_status,
                constant.BLOG_MODEL_FIELDS['like']
            )
        except:
            blog_details['current_user_like_status'] = 0

        get_comment_data_filter = {
            constant.BLOG_MODEL_FIELDS['blog']: getattr(blog, constant.BLOG_MODEL_FIELDS['blog_id']),
        }
        get_comment_data = CommentMaster.objects.filter(**get_comment_data_filter)
        blog_details['total_comment'] = len(get_comment_data)
        user_details = []
        for comment in get_comment_data:
            user_id = getattr(comment, constant.BLOG_MODEL_FIELDS["comment_by"])
            auth_id = AuthUser.objects.get(
                email=user_id
            )
            get_user = MasterUser.objects.filter(**{constant.USER_MODEL_FIELDS['user']: auth_id})[:1].get()
            user_name = my_name_create(get_user)

            user_comment = getattr(
                comment,
                constant.BLOG_MODEL_FIELDS['comment']
            )
            user_detail_dict = {'id': auth_id.id, 'name': user_name, 'comment': user_comment}
            user_details.append(user_detail_dict)
        blog_details['total_user_comment'] = user_details
        total_blog_details.append(blog_details)

    blog_serializer = BlogSerializer(get_blogs, many=True)
    n = len(get_blogs)
    nSlid = n // 4 + ceil((n / 4) - (n // 4))
    alert = constant.GET_ALL_BLOG_DATA_SUCCESSFUL
    params = {'no_of_slides': nSlid, 'total blogs': total_blogs, 'blogs_detail': total_blog_details}
    return my_response_create(alert=alert, result=True, data=params)


def create_blog(request=None, user_id=None):
    if not request:
        my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)
    get_json_data = loads(request.body)
    if not constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data and \
            not constant.BLOG_MODEL_FIELDS['blog_image'] in get_json_data:
        alert = f"{constant.ONE_FIELD_REQUIRED_FROM_FIELDS} {constant.BLOG_MODEL_FIELDS['blog_title']}" + \
                f" and {constant.BLOG_MODEL_FIELDS['blog_image']}!"
        return my_response_create(result=False, alert=alert)
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
        create_new_blog = BlogMaster(**blog_params)
        create_new_blog.save()
        return my_response_create(result=True, alert=constant.CREATE_BLOG_SUCCESSFUL)
    except:
        return my_response_create(result=False, alert=constant.DATABASE_SERVER_ERROR)


def update_blog(request=None, user_id=None):
    if request is None:
        my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)
    get_json_data = loads(request.body)

    if not constant.BLOG_MODEL_FIELDS['get_blog_id'] in get_json_data:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)

    if not constant.BLOG_MODEL_FIELDS['blog_title'] in get_json_data and \
            not constant.BLOG_MODEL_FIELDS['blog_desc'] in get_json_data:
        alert = f"{constant.ONE_FIELD_REQUIRED_FROM_FIELDS} {constant.BLOG_MODEL_FIELDS['blog_title']}" + \
                f" and {constant.BLOG_MODEL_FIELDS['blog_desc']}!"
        return my_response_create(result=False, alert=alert)

    blog_id = get_json_data['blog_id']
    blog_filter = {constant.BLOG_MODEL_FIELDS['blog_id']: blog_id}
    get_blog = BlogMaster.objects.filter(**blog_filter)
    if not get_blog:
        return my_response_create(result=False, alert=constant.BLOG_NOT_EXIST)

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
        return my_response_create(result=False, alert=constant.UPDATE_FAIL)
    return my_response_create(result=True, alert=constant.BLOG_UPDATE_SUCCESSFUL)


def delete_blog(request, user_id=None):
    if not request or not request.body:
        my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)
    try:
        get_json_data = loads(request.body)
    except:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)

    if not constant.BLOG_MODEL_FIELDS['get_blog_id'] in get_json_data:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)

    blog_id = get_json_data[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    blog_filter = {
        constant.BLOG_MODEL_FIELDS['blog_id']: blog_id,
        constant.BLOG_MODEL_FIELDS['blog_delete']: constant.BLOG_NOT_DELETE_NUM,
        constant.BLOG_MODEL_FIELDS['blog_created_by']: user_id
    }
    get_blog = BlogMaster.objects.filter(**blog_filter)
    if not get_blog:
        return my_response_create(result=False, alert=constant.BLOG_NOT_EXIST)
    try:
        # get_blog.update(**{constant.BLOG_MODEL_FIELDS['blog_delete']: constant.BLOG_DELETE_NUM})
        get_blog.delete()
    except:
        return my_response_create(result=False, alert=constant.BLOG_NOT_DELETE)

    return my_response_create(result=True, alert=constant.BLOG_DELETE_SUCCESSFUL)


def like_blog(request=None, user_id=None):
    if not request:
        my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)

    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)
    get_json_response = loads(request.body)

    if constant.BLOG_MODEL_FIELDS['get_blog_id'] and constant.BLOG_MODEL_FIELDS['like_status'] not in get_json_response:
        alert = my_payload_error(
            constant.BLOG_MODEL_FIELDS['get_blog_id'],
            constant.BLOG_MODEL_FIELDS['like_status']
        )
        return my_response_create(result=False, alert=alert)

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
    get_like_blog = LikeMaster.objects.filter(**like_filter)
    like_params = {constant.BLOG_MODEL_FIELDS['like']: get_like_status}
    if get_like_blog:
        get_like_blog.update(**like_params)
    else:
        get_user = AuthUser.objects.get(**{constant.USER_MODEL_FIELDS['id']: user_id})
        try:
            get_blog = BlogMaster.objects.get(**{constant.BLOG_MODEL_FIELDS['blog_id']: blog_id})
        except:
            return my_response_create(result=False, alert=constant.BLOG_NOT_EXIST)
        like_params[constant.BLOG_MODEL_FIELDS['like_by']] = get_user
        like_params[constant.BLOG_MODEL_FIELDS['blog']] = get_blog
        like_blog = LikeMaster(**like_params)
        like_blog.save()

    return my_response_create(result=True, alert=alert)


def comment_blog(request=None, user_id=None):
    if not request:
        return my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)

    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)
    get_json_response = loads(request.body)
    if constant.BLOG_MODEL_FIELDS['get_blog_id'] not in get_json_response \
            or constant.BLOG_MODEL_FIELDS['comment'] not in get_json_response:
        alert = my_payload_error(
            constant.BLOG_MODEL_FIELDS['get_blog_id'], constant.BLOG_MODEL_FIELDS['comment']
        )
        return my_response_create(result=False, alert=alert)

    blog_id = get_json_response[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    comment = get_json_response[constant.BLOG_MODEL_FIELDS['comment']].capitalize()

    comment_filter = {
        constant.BLOG_MODEL_FIELDS['comment_by']: user_id,
        constant.BLOG_MODEL_FIELDS['blog']: blog_id
    }
    blog_comment = CommentMaster.objects.filter(**comment_filter)
    if not blog_comment:
        try:
            get_blog = BlogMaster.objects.get(**{constant.BLOG_MODEL_FIELDS['blog_id']: blog_id})
        except:
            return my_response_create(result=False, alert=constant.BLOG_NOT_EXIST)
        get_user = AuthUser.objects.filter(**{constant.USER_MODEL_FIELDS['id']: user_id})[:1].get()
        comment_params = {
            constant.BLOG_MODEL_FIELDS['blog']: get_blog,
            constant.BLOG_MODEL_FIELDS['comment_by']: get_user,
            constant.BLOG_MODEL_FIELDS['comment']: comment
        }
        comment_object = CommentMaster(**comment_params)
        comment_object.save()
        alert = constant.CREATE_COMMENT_SUCCESSFUL
    else:
        comment_params = {
            constant.BLOG_MODEL_FIELDS['comment']: comment
        }
        blog_comment.update(**comment_params)
        alert = constant.UPDATE_COMMENT_SUCCESSFUL
    return my_response_create(result=True, alert=alert)


def delete_comment_blog(request=None, user_id=None):
    if not request:
        return my_response_create(result=False, alert=constant.UNEXPECTED_ERROR)
    # user_id = my_session_get(request=request, key=constant.SESSION_USER_ID)
    # if not user_id:
    #     return my_response_create(result=False, alert=constant.USER_NOT_LOGGED_IN)

    if not request.body:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)

    get_json_response = loads(request.body)
    if constant.BLOG_MODEL_FIELDS['get_blog_id'] not in get_json_response:
        alert = my_payload_error(constant.BLOG_MODEL_FIELDS['get_blog_id'])
        return my_response_create(result=False, alert=alert)

    blog_id = get_json_response[constant.BLOG_MODEL_FIELDS['get_blog_id']]
    comment_filter = {
        constant.BLOG_MODEL_FIELDS['comment_by']: user_id,
        constant.BLOG_MODEL_FIELDS['blog']: blog_id
    }
    get_comment = CommentMaster.objects.filter(**comment_filter)
    if not get_comment:
        return my_response_create(result=False, alert=constant.COMMENT_NOT_EXIST)
    get_comment.delete()
    return my_response_create(result=True, alert=constant.DELETE_COMMENT_SUCCESSFUL)
