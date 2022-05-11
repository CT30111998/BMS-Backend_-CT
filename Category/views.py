from rest_framework.views import APIView
from Auth.jwt_module import JWTAuthentication
from .modules import get_all_cat, create_category
from BMSystem.base_function import get_user_id_from_request
from base.common_helpers import create_response
from BMSystem import response_messages

# Create your views here.


class Category(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def get(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = get_all_cat(request, user_id)
        return get_response

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = create_category(request, user_id)
        return get_response

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = create_category(request, user_id)
        return get_response
