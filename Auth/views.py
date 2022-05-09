from rest_framework.views import APIView
from base.common_helpers import create_response
from .serializers import CreateUserSerializer, LoginSerializer
from BMSystem import constants, response_messages, decimal_constants, model_fields
from .jwt_module import jwt_encode, generate_key, logout as session_logout, JWTAuthentication, get_token_from_request
from django.utils import timezone
from base.query_modules import save_data, get_data, update_data_by_fields
from .models import AuthMaster, AuthToken, GroupMaster
from User.models import UserMaster, UserGroup
from datetime import datetime
from base.common_helpers import convert_time_to_timestamp


class SignUp(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = CreateUserSerializer
        self.authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            fields = serializer.data
            del fields['confirm_password']
            first_auth_object = get_data(model=AuthMaster)
            if not first_auth_object:
                group_object = get_data(model=GroupMaster, filters={model_fields.ID: decimal_constants.OWNER})
            else:
                group_object = get_data(model=GroupMaster, filters={model_fields.ID: decimal_constants.USER})
            auth_data_object = save_data(model=AuthMaster, fields=fields)
            if not data:
                return create_response(alert=response_messages.UNEXPECTED_ERROR)

            del fields[model_fields.PASSWORD], fields[model_fields.IS_ACTIVE], fields[model_fields.IS_DELETED]

            try:
                fields.update({
                    model_fields.FIRST_NAME: data[model_fields.FIRST_NAME],
                    model_fields.LAST_NAME: data[model_fields.LAST_NAME],
                    model_fields.MOBILE_NUMBER: data[model_fields.MOBILE_NUMBER],
                    model_fields.USER: auth_data_object,
                    model_fields.CREATED_AT: timezone.now()
                })
                user_data_object = save_data(model=UserMaster, fields=fields)
                if not user_data_object:
                    auth_data_object.delete()
                    return create_response(alert=response_messages.UNEXPECTED_ERROR)
            except:
                auth_data_object.delete()
                return create_response(alert=response_messages.UNEXPECTED_ERROR)

            user_group_object = save_data(model=UserGroup, fields={
                'group': group_object.first(),
                model_fields.USER: auth_data_object,
                model_fields.CREATED_AT: timezone.now()
            })
            if not user_group_object:
                auth_data_object.delete()
                user_data_object.delete()
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
                'token': encode_key,
                'user_master': user_object.first(),
                'created_at': timezone.now()
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
        key = get_token_from_request(request)

        session_object = get_data(model=AuthToken, filters={'token': key})
        if not session_object:
            return create_response(alert=response_messages.USER_NOT_LOGGED_IN)

        status = session_logout(session_object=session_object)
        if not status:
            return create_response(alert=response_messages.UNEXPECTED_ERROR)

        return create_response(alert=response_messages.LOGOUT_SUCCESSFUL)
