from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from Blog.modules import *
from os import SEEK_END
from .models import BlogMaster as Master
from BMSystem import response_messages, model_fields
from base.common_helpers import create_response
from BMSystem.base_function import get_user_id_from_request, check_response_result
from Auth.jwt_module import JWTAuthentication
# from .serializer import BlogSerializer


class BlogMaster(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = BlogSerializer
        self.authentication_classes = [JWTAuthentication]

    def list(self, request):
        user_id = get_user_id_from_request(request)

        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        blog_id = request.GET.get('blog_id', None)
        get_response = get_all_blog(blog_id=blog_id, serializer_class=self.serializer_class)
        return get_response

    def retrieve(self, request, blog_id):
        user_id = get_user_id_from_request(request)

        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        get_response = get_all_blog(blog_id=blog_id, serializer_class=self.serializer_class)
        return get_response

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        if not request.data:
            alert = my_payload_error(model_fields.BLOG_ID)
            return create_response(alert=alert)

        get_response = create_blog(request_date=request.data, user_id=user_id)
        return get_response

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)

        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        if not request.data:
            alert = my_payload_error(model_fields.BLOG_ID)
            return my_response_create(result=False, alert=alert)

        get_response = update_blog(request.data)
        return get_response

    @staticmethod
    def delete(request):
        user_id = get_user_id_from_request(request)

        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        blog_id = request.GET.get('blog_id', None)
        get_response = delete_blog(blog_id=blog_id, user_id=user_id)
        return get_response


class LikBlog(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.serializer_class = BlogSerializer
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = like_blog(request_data=request.data, user_id=user_id)
        return get_response

    @staticmethod
    def put(self, request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = like_blog(request_data=request.data, user_id=user_id)
        return get_response


class CommentBlog(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = comment_blog(request_data=request.data, user_id=user_id)
        return get_response

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)
        get_response = comment_blog(request_data=request.data, user_id=user_id)
        return get_response

    @staticmethod
    def delete(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        blog_id = request.GET.get('blog_id', None)
        get_response = delete_comment_blog(blog_id=blog_id, user_id=user_id)
        return get_response


# @api_view(['POST'])
# def upload_file(request, blog_id=None):
#     file = request.FILES['file']
#     user_id = request.POST['user_id']
#     print("FILE TYPE: ", file.content_type)
#     if file.content_type not in constants.IMAGE_MIME_TYPES:
#         return create_response(alert=response_messages.INVALID_FILE_TYPE)
#
#     file.seek(0, SEEK_END)
#     size = file.tell()
#     file.seek(0)
#     if size >= constants.MAX_FILE_SIZE:
#         return create_response(alert=response_messages.MAX_FILE_SIZE_LIMIT_REACHED)
#     fs = FileSystemStorage()
#     path = f"{constants.UPLOAD_PATH}{constants.BLOG_PATH}{file.name}"
#     fs.save(name=path, content=file)
#
#     blog_filter = {model_fields.ID: blog_id}
#     get_blog = Master.objects.filter(**blog_filter)
#     if not get_blog:
#         return create_response(result=False, alert=response_messages.BLOG_NOT_EXIST)
#     get_blog.update(**{'postImage': path})
#     # session = Session(aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET_KEY)
#     # s3 = session.resource(constants.CONST_DICT['S3'])
#     # file_obj = s3.Object(S3_BUCKET_NAME, file.name)
#     # upload_status = file_obj.put(Body=file)
#     #
#     # if not upload_status:
#     #     return create_response(code=constants.RESPONSE_CODES['FILE_UPLOAD_FAILURE'])
#     return create_response(alert=response_messages.FILE_UPLOAD_SUCCESS, data={'file_url': 'Image.jpg'})
# # except:
# #     return create_response(alert=constants.FILE_UPLOAD_FAILURE)
