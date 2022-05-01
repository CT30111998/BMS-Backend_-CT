from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Blog.modules import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
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
