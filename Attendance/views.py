from rest_framework.viewsets import ViewSet
from Auth.jwt_module import JWTAuthentication
from .modules import get_all_user_attendance, create_update_attendance, delete_user_attendance
from BMSystem.base_function import get_user_id_from_request
from base.common_helpers import create_response
from BMSystem import response_messages


class Attendance(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    @staticmethod
    def list(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = get_all_user_attendance(request_data=request.GET, user_id=user_id)
        return get_response

    @staticmethod
    def retrieve(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)

        # get_response = get_user_attendance(request, user_id)
        return create_response(result=True)

    @staticmethod
    def post(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = create_update_attendance(request.data, user_id)
        return get_response

    @staticmethod
    def put(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = create_update_attendance(request.data, user_id)
        return get_response

    @staticmethod
    def delete(request):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return create_response(result=False, alert=response_messages.USER_NOT_LOGGED_IN)

        get_response = delete_user_attendance(request.data)
        return get_response
