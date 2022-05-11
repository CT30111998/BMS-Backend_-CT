from rest_framework.views import APIView
from Auth.jwt_module import JWTAuthentication
from .modules import api_create_update_depart, api_get_department, api_delete_department
from BMSystem.base_function import get_user_id_from_request
from base.common_helpers import create_response
from BMSystem import response_messages


class Department(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def get(request):
        return api_get_department(request.GET)

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return api_create_update_depart(request_data=request.data, user_id=user_id)

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return api_create_update_depart(request_data=request.data, user_id=user_id)

    @staticmethod
    def delete(request):
        department_id = request.GET.get('department_id', None)
        if not department_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)
        return api_delete_department(department_id=department_id)
