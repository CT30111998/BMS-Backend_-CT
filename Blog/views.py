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


class UpdateBlog(APIView):

    def delete(self, request=None, blog_id=None):
        get_response = delete_blog(request=request, blog_id=blog_id)
        return get_response

    def put(self, request=None, blog_id=None):
        get_response = update_blog(request=request, blog_id=blog_id)
        return get_response


class LikBlog(APIView):

    def post(self, request, blog_id):
        get_response = create_like_blog(request=request, blog_id=blog_id)
        return get_response

    def put(self, request, blog_id):
        get_response = update_like_blog(request=request, blog_id=blog_id)
        return get_response
