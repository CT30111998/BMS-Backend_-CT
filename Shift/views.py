from rest_framework.views import APIView
from Auth.jwt_module import JWTAuthentication
from .modules import (
    api_create_update_shift, api_get_shift, api_delete_shift
)
from base.common_helpers import create_response, get_user_id_from_request
from BMSystem import response_messages


class Shift(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def get(request):
        return api_get_shift(request.GET)

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return api_create_update_shift(request_data=request.data, user_id=user_id)

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return api_create_update_shift(request_data=request.data, user_id=user_id)

    @staticmethod
    def delete(request):
        shift_id = request.GET.get('shift_id', None)
        if not shift_id:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)
        return api_delete_shift(shift_id=shift_id)


# class UserDepartment(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.authentication_classes = [JWTAuthentication]
#
#     @staticmethod
#     def get(request):
#         return api_get_user_department()
#
#     @staticmethod
#     def post(request):
#         user_id = get_user_id_from_request(request)
#         if not user_id:
#             return create_response(alert=response_messages.UNEXPECTED_ERROR)
#
#         return api_create_user_department(request_data=request.data, user_id=user_id)
#
#     @staticmethod
#     def put(request):
#         user_id = get_user_id_from_request(request)
#         if not user_id:
#             return create_response(alert=response_messages.UNEXPECTED_ERROR)
#         return api_update_user_department(request_data=request.data, user_id=user_id)
#
#     @staticmethod
#     def delete(request):
#         return api_delete_user_department(request_data=request.GET)
