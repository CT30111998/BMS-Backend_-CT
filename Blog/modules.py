# Blog Modules
import datetime
from django.core.files.storage import FileSystemStorage
from .models import BlogMaster as BlogMaster, BlogLike as LikeMaster, BlogComment as CommentMaster
from math import ceil
from Auth.models import AuthMaster as AuthUser
from base.query_modules import get_data, save_data, update_data_by_fields
from BMSystem import constants, response_messages, model_fields, decimal_constants
from base.common_helpers import create_response as my_response_create,\
    get_payload_error_alert as my_payload_error
from django.utils import timezone
from .serializers import BlogSerializer


def get_all_blog(serializer_class=None, blog_id=None):
    blog_filter = {
        model_fields.IS_DELETED: decimal_constants.NOT_DELETED,
    }
    if blog_id:
        blog_filter['id'] = blog_id

    get_blogs = get_data(model=BlogMaster, filters=blog_filter)
    if not get_blogs:
        return my_response_create(alert=response_messages.BLOG_NOT_EXIST)
    total_blogs = len(get_blogs)
    total_blog_details = []

    # for blog in get_blogs:
    #     blog_details = {}
    #
    #     get_user_filter = {
    #         model_fields.USER: getattr(blog, model_fields.CREATED_BY)
    #     }
    #     get_user = MasterUser.objects.get(**get_user_filter)
    #     get_user_id = getattr(get_user, model_fields.ID)
    #     user_name = my_name_create(get_user)
    #
    #     blog_details['blog_id'] = getattr(blog, model_fields.ID)
    #     blog_details['blog_image'] = str(getattr(blog, model_fields.BLOG_IMAGE))
    #     blog_details['blog_title'] = getattr(blog, model_fields.BLOG_TITLE)
    #     blog_details['blog_desc'] = getattr(blog, model_fields.BLOG_TITLE)
    #     blog_details['blog_created_by'] = {'id': get_user_id, 'name': user_name}
    #     blog_details['blog_modify_at'] = getattr(blog, model_fields.UPDATED_AT)
    #
    #     get_like_data_filter = {
    #         model_fields.BLOG: getattr(blog, model_fields.ID),
    #         model_fields.LIKE: decimal_constants.LIKE
    #     }
    #     get_likes_data = LikeMaster.objects.filter(**get_like_data_filter)
    #     blog_details['total_like_count'] = len(get_likes_data)
    #
    #     user_like_details = []
    #     for get_total_like in get_likes_data:
    #         user_id = getattr(get_total_like, model_fields.CREATED_BY)
    #         auth_id = AuthUser.objects.get(
    #             email=user_id
    #         )
    #         get_user = MasterUser.objects.get(user=user_id)
    #         user_name = my_name_create(get_user)
    #         user_detail_dict = {'id': getattr(auth_id, model_fields.ID), 'name': user_name}
    #         user_like_details.append(user_detail_dict)
    #
    #     blog_details['total_user_like'] = user_like_details
    #     like_filter = {
    #         model_fields.BLOG: getattr(blog, model_fields.ID),
    #         model_fields.CREATED_BY: my_session_get(
    #             request=request,
    #             key=model_fields.USER_ID)}
    #     try:
    #         current_user_like_status = LikeMaster.objects.filter(**like_filter)[:1].get()
    #         blog_details['current_user_like_status'] = getattr(
    #             current_user_like_status,
    #             model_fields.LIKE
    #         )
    #     except:
    #         blog_details['current_user_like_status'] = 0
    #
    #     get_comment_data_filter = {
    #         model_fields.BLOG: getattr(blog, model_fields.ID),
    #     }
    #     get_comment_data = CommentMaster.objects.filter(**get_comment_data_filter)
    #     blog_details['total_comment'] = len(get_comment_data)
    #     user_details = []
    #     for comment in get_comment_data:
    #         user_id = getattr(comment, model_fields.CREATED_BY)
    #         auth_id = AuthUser.objects.get(
    #             email=user_id
    #         )
    #         get_user = MasterUser.objects.filter(**{model_fields.USER: auth_id})[:1].get()
    #         user_name = my_name_create(get_user)
    #
    #         user_comment = getattr(
    #             comment,
    #             model_fields.COMMENT
    #         )
    #         user_detail_dict = {'id': auth_id.id, 'name': user_name, 'comment': user_comment}
    #         user_details.append(user_detail_dict)
    #     blog_details['total_user_comment'] = user_details
    #     total_blog_details.append(blog_details)

    blog_serializer = serializer_class(get_blogs, many=True)
    n = len(get_blogs)
    n_slide = n // 4 + ceil((n / 4) - (n // 4))
    alert = response_messages.GET_ALL_BLOG_DATA_SUCCESSFUL
    params = {'no_of_slides': n_slide, 'total blogs': total_blogs, 'blogs_detail': blog_serializer.data}
    if total_blogs == 1:
        params['blogs_detail'] = blog_serializer.data[0]
    return my_response_create(alert=alert, result=True, data=params)


def create_blog(request_date=None, user_id=None):
    if not model_fields.BLOG_TITLE and model_fields.BLOG_IMAGE in request_date:
        alert = f"{response_messages.ONE_FIELD_REQUIRED_FROM_FIELDS} {model_fields.BLOG_TITLE}" + \
                f" and {model_fields.BLOG_IMAGE}!"
        return my_response_create(result=False, alert=alert)

    user_object = get_data(model=AuthUser, filters={model_fields.ID: user_id}).first()
    blog_create_params = {model_fields.CREATED_BY: user_object}

    if model_fields.BLOG_TITLE in request_date:
        blog_create_params[model_fields.BLOG_TITLE] = \
            request_date[model_fields.BLOG_TITLE].title()

    if model_fields.BLOG_DESC in request_date:
        blog_create_params[model_fields.BLOG_DESC] = \
            request_date[model_fields.BLOG_DESC].capitalize()

    if model_fields.BLOG_IMAGE in request_date:
        get_file = request_date.FILES['postImage']
        fs = FileSystemStorage()
        time = str(datetime.datetime.now())
        time_str = time.split('.')[0].replace(' ', '-').replace(':', '-')
        path = f"{constants.UPLOAD_PATH}{constants.BLOG_PATH}{time_str}_{get_file.name}"
        fs.save(name=path, content=get_file)
        blog_create_params[model_fields.BLOG_IMAGE] = constants.MEDIA_PATH + path

    blog_create_params[model_fields.CREATED_AT] = timezone.now()

    create_new_blog = save_data(model=BlogMaster, fields=blog_create_params)
    if not create_new_blog:
        return my_response_create(result=False, alert=response_messages.UNEXPECTED_ERROR)
    return my_response_create(result=True, alert=response_messages.CREATE_BLOG_SUCCESSFUL)


def update_blog(request_data=None):
    if not str(model_fields.BLOG_TITLE) in request_data and not str(model_fields.BLOG_DESC) in request_data:
        alert = f"{response_messages.ONE_FIELD_REQUIRED_FROM_FIELDS} {model_fields.BLOG_TITLE}" + \
                f" and {model_fields.BLOG_DESC}!"
        return my_response_create(alert=alert)

    blog_id = request_data.get('blog_id', None)
    blog_object = get_data(model=BlogMaster, filters={model_fields.ID: blog_id})
    if not blog_object:
        return my_response_create(result=False, alert=response_messages.BLOG_NOT_EXIST)

    blog_params = {model_fields.CREATED_AT: timezone.now()}

    if model_fields.BLOG_TITLE in request_data:
        blog_params[model_fields.BLOG_TITLE] = \
            request_data[model_fields.BLOG_TITLE].title()
    if model_fields.BLOG_DESC in request_data:
        blog_params[model_fields.BLOG_DESC] = \
            request_data[model_fields.BLOG_DESC].capitalize()

    blog_update = update_data_by_fields(model_object=blog_object, fields=blog_params)
    return my_response_create(result=True, alert=response_messages.BLOG_UPDATE_SUCCESSFUL)


def delete_blog(blog_id=None, user_id=None):
    blog_filter = {
        model_fields.ID: blog_id,
        model_fields.IS_DELETED: decimal_constants.BLOG_NOT_DELETE_NUM,
        model_fields.CREATED_BY: user_id
    }
    blog_object = get_data(model=BlogMaster, filters=blog_filter)
    if not blog_object:
        return my_response_create(result=False, alert=response_messages.BLOG_NOT_EXIST)

    blog_object.delete()

    return my_response_create(result=True, alert=response_messages.BLOG_DELETE_SUCCESSFUL)


def like_blog(request_data=None, user_id=None):
    blog_id = request_data.get('blog_id', None)
    like_status = request_data[model_fields.LIKE_STATUS] \
        if model_fields.LIKE_STATUS in request_data else str(decimal_constants.UNLIKE)

    user_object = get_data(model=AuthUser, filters={model_fields.ID: user_id})
    if not user_object:
        return my_response_create(alert=response_messages.UNEXPECTED_ERROR)

    like_filter = {
        model_fields.BLOG: blog_id,
        model_fields.CREATED_BY: user_id,
    }
    alert = response_messages.BLOG_LIKE_SUCCESSFUL
    if like_status == str(decimal_constants.UNLIKE):
        alert = response_messages.BLOG_UNLIKE_SUCCESSFUL

    blog_object = get_data(model=LikeMaster, filters=like_filter)
    like_params = {model_fields.LIKE: like_status}

    if blog_object:
        blog_object.update(**like_params)
    else:
        blog_object = get_data(model=BlogMaster, filters={model_fields.ID: blog_id})
        if not blog_object:
            return my_response_create(result=False, alert=response_messages.BLOG_NOT_EXIST)

        like_params.update({
            model_fields.CREATED_BY: user_object.first(),
            model_fields.BLOG: blog_object.first(),
            model_fields.CREATED_AT: timezone.now()
        })
        save_data(model=LikeMaster, fields=like_params)

    return my_response_create(result=True, alert=alert)


def comment_blog(request_data=None, user_id=None):

    if model_fields.BLOG_ID not in request_data \
            or model_fields.COMMENT not in request_data:
        alert = my_payload_error(
            model_fields.BLOG_ID, model_fields.COMMENT
        )
        return my_response_create(result=False, alert=alert)

    blog_id = request_data[model_fields.BLOG_ID]
    comment = request_data[model_fields.COMMENT].capitalize()

    comment_filter = {
        model_fields.CREATED_BY: user_id,
        model_fields.BLOG: blog_id
    }
    blog_comment_object = get_data(model=CommentMaster, filters=comment_filter)
    if not blog_comment_object:
        blog_object = get_data(model=BlogMaster, filters={model_fields.ID: blog_id})
        if not blog_object:
            return my_response_create(result=False, alert=response_messages.BLOG_NOT_EXIST)

        user_object = get_data(model=AuthUser, filters={model_fields.ID: user_id})
        comment_params = {
            model_fields.BLOG: blog_object.first(),
            model_fields.CREATED_BY: user_object.first(),
            model_fields.COMMENT: comment,
            model_fields.CREATED_AT: timezone.now()
        }
        save_data(model=CommentMaster, fields=comment_params)
        alert = response_messages.CREATE_COMMENT_SUCCESSFUL
    else:
        comment_params = {
            model_fields.COMMENT: comment,
            model_fields.CREATED_AT: timezone.now()
        }
        update_data_by_fields(model_object=blog_comment_object, fields=comment_params)
        alert = response_messages.UPDATE_COMMENT_SUCCESSFUL
    return my_response_create(result=True, alert=alert)


def delete_comment_blog(blog_id=None, user_id=None):
    comment_filter = {
        model_fields.CREATED_BY: user_id,
        model_fields.BLOG: blog_id
    }
    comment_object = get_data(model=CommentMaster, filters=comment_filter)
    if not comment_object:
        return my_response_create(result=False, alert=response_messages.COMMENT_NOT_EXIST)

    comment_object.delete()
    return my_response_create(result=True, alert=response_messages.DELETE_COMMENT_SUCCESSFUL)
