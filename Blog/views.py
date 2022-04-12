from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Blog.modules import *


class BlogMaster(APIView):
    def get(self, request):
        get_response = get_all_blog(request)
        return get_response

    def post(self, request):
        get_response = create_blog(request)
        return get_response
