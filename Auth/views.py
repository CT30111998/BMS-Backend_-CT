from rest_framework.views import APIView
from base.common_helpers import create_response
from .serializer import CreateUserSerializer, LoginSerializer
from BMSystem import constants, response_messages, decimal_constants
from .jwt_module import jwt_encode, generate_key, logout as session_logout, JWTAuthentication
from django.utils import timezone
from base.query_modules import save_data, get_data, update_data_by_fields
from .models import AuthMaster, AuthToken
from datetime import datetime
from base.common_helpers import convert_time_to_timestamp


class SignUp(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = CreateUserSerializer
        self.authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            fields = serializer.data
            del fields['confirm_password']

            status, data = save_data(model=AuthMaster, fields=fields)
            if not status:
                return create_response(alert=response_messages.UNEXPECTED_ERROR)

            return create_response(alert=response_messages.REGISTER_SUCCESSFUL)
        else:
            return create_response(alert=serializer.errors)


class Login(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = LoginSerializer
        self.authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Encode key
            encode_key = jwt_encode({'key': generate_key()})

            # Get current user
            user_object = get_data(model=AuthMaster, filters={'email': serializer.data['email']})

            # Create session
            save_data(model=AuthToken, fields={
                'key': encode_key,
                'user_master': user_object.first(),
                'created_at': datetime.timestamp(datetime.now())
            })

            # Update user to Active
            update_data_by_fields(model_object=user_object, fields={'is_active': decimal_constants.ACTIVE})
            return create_response(alert=response_messages.LOGIN_SUCCESSFUL, data={'access': encode_key})
        else:
            return create_response(alert=serializer.errors)


class Logout(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_classes = [JWTAuthentication]

    def post(self, request):
        key = request.META['HTTP_AUTHORIZATION']
        session_object = get_data(model=AuthToken, filters={'key': key})
        if not session_object:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        status = session_logout(session_object=session_object)
        if not status:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return create_response(alert=response_messages.LOGOUT_SUCCESSFUL)
