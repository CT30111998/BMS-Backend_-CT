import jwt
from BMSystem import constants, response_messages, decimal_constants
from BMSystem.settings import SECRET_KEY
import binascii
import os
from Auth.models import AuthToken, AuthMaster
from base.query_modules import get_data, save_data, update_data_by_fields
from datetime import datetime
from BMSystem import settings
from django.utils import timezone
from rest_framework import authentication, exceptions
from base.common_helpers import convert_time_to_timestamp
from binascii import hexlify
from BMSystem.settings import TOKEN_KEY_LENGTH
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from BMSystem.settings import SESSION_LENGTH


def jwt_encode(payload):
    return jwt.encode(payload=payload, key=SECRET_KEY)


def jwt_decode(encode_data):
    return jwt.decode(encode_data, key=SECRET_KEY, algorithms=['HS256'])


def generate_key():
    return hexlify(os.urandom(20)).decode()


class JWTAuthentication(TokenAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        # Get Key from HTTP header
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise AuthenticationFailed(response_messages.AUTHORIZATION_ERROR)

        status, session_object = get_data(model=AuthToken, filters={'token': token})
        if not session_object:
            raise AuthenticationFailed(response_messages.AUTHORIZATION_ERROR)

        if convert_time_to_timestamp() - session_object.first().created_time > SESSION_LENGTH:
            logout(session_object=session_object)
            raise AuthenticationFailed(response_messages.AUTHORIZATION_ERROR)
        return str(session_object.first().token), None


def logout(session_object=None):
    # Update user active status.
    user = get_data(model=AuthMaster, filters={'id': session_object.first().user_master.id})
    if not user:
        return False

    status = update_data_by_fields(model_object=user, fields={'is_active': decimal_constants.NOT_ACTIVE})
    if not status:
        return status

    # Delete session
    user.delete()

    return status
