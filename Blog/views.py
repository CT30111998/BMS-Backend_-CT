from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Blog.modules import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


class BlogMaster(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        get_response = get_all_blog(request)
        return get_response

    @csrf_exempt
    def post(self, request):
        get_response = create_blog(request)
        return get_response

    def put(self, request=None):
        get_response = update_blog(request=request)
        return get_response

    def delete(self, request):
        get_response = delete_blog(request=request)
        return get_response


class UpdateBlog(APIView):
    def get(self, request):
        get_response = delete_blog(request=request)
        return get_response


class LikBlog(APIView):

    def post(self, request):
        get_response = like_blog(request=request)
        return get_response

    def put(self, request):
        get_response = like_blog(request=request)
        return get_response


class CommentBlog(APIView):

    def post(self, request):
        get_response = comment_blog(request)
        return get_response

    def put(self, request):
        get_response = comment_blog(request)
        return get_response

    def delete(self, request):
        get_response = delete_comment_blog(request)
        return get_response
