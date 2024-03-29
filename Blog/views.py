from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response
from Blog.modules import *
from os import SEEK_END
from .models import Master
from BMSystem.base_function import check_user_loging, check_response_result, create_response


class BlogMaster(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.UNEXPECTED_ERROR)
        # user_id = request.GET['user_id']
        get_response = get_all_blog(request, user_id)
        return get_response

    # @csrf_exempt
    def post(self, request, user_id=None):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.UNEXPECTED_ERROR)
        get_response = create_blog(request, user_id)
        return get_response

    def put(self, request=None, user_id=None):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.UNEXPECTED_ERROR)
        get_response = update_blog(request, user_id)
        return get_response

    def delete(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        # user_id = request.GET['user_id']
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = delete_blog(request=request, user_id=user_id)
        return get_response


class UpdateBlog(APIView):
    def get(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = delete_blog(request=request, user_id=user_id)
        return get_response


class LikBlog(APIView):

    def post(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = like_blog(request=request, user_id=user_id)
        return get_response

    def put(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = like_blog(request=request, user_id=user_id)
        return get_response


class CommentBlog(APIView):

    def post(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = comment_blog(request, user_id)
        return get_response

    def put(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = comment_blog(request, user_id)
        return get_response

    def delete(self, request):
        user_id = check_user_loging(request)
        # user_id = check_response_result(response)
        if not user_id:
            return create_response(alert=constants.USER_NOT_LOGGED_IN)
        get_response = delete_comment_blog(request, user_id)
        return get_response


@api_view(['POST'])
def upload_file(request, blog_id=None):
    file = request.FILES['file']
    user_id = request.POST['user_id']
    print("FILE TYPE: ", file.content_type)
    if file.content_type not in constants.IMAGE_MIME_TYPES:
        return create_response(alert=constants.INVALID_FILE_TYPE)

    file.seek(0, SEEK_END)
    size = file.tell()
    file.seek(0)
    if size >= constants.MAX_FILE_SIZE:
        return create_response(alert=constants.MAX_FILE_SIZE_LIMIT_REACHED)
    fs = FileSystemStorage()
    path = f"{constants.UPLOAD_PATH}{constants.BLOG_PATH}{file.name}"
    fs.save(name=path, content=file)

    blog_filter = {constants.BLOG_MODEL_FIELDS['blog_id']: blog_id}
    get_blog = Master.objects.filter(**blog_filter)
    if not get_blog:
        return my_response_create(result=False, alert=constants.BLOG_NOT_EXIST)
    get_blog.update(**{'postImage': path})
    # session = Session(aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET_KEY)
    # s3 = session.resource(constants.CONST_DICT['S3'])
    # file_obj = s3.Object(S3_BUCKET_NAME, file.name)
    # upload_status = file_obj.put(Body=file)
    #
    # if not upload_status:
    #     return create_response(code=constants.RESPONSE_CODES['FILE_UPLOAD_FAILURE'])
    return create_response(alert=constants.FILE_UPLOAD_SUCCESS, data={'file_url': 'Image.jpg'})
# except:
#     return create_response(alert=constants.FILE_UPLOAD_FAILURE)
