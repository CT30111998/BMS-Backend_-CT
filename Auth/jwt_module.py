import jwt
from BMSystem import constants, response_messages, decimal_constants, model_fields
from BMSystem.settings import SECRET_KEY
import os
from Auth.models import AuthToken, AuthMaster
from base.query_modules import get_data, save_data, update_data_by_fields
from base.common_helpers import convert_time_to_timestamp
from binascii import hexlify
from BMSystem.settings import TOKEN_KEY_LENGTH
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from BMSystem.settings import SESSION_LENGTH
from django.utils import timezone


def jwt_encode(payload):
    return jwt.encode(payload=payload, key=SECRET_KEY)


def jwt_decode(encode_data):
    return jwt.decode(encode_data, key=SECRET_KEY, algorithms=['HS256'])


def generate_key():
    return hexlify(os.urandom(20)).decode()


class JWTAuthentication(TokenAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):

        if 'email' in request.data:
            user_object = get_data(model=AuthMaster, filters={model_fields.IS_ACTIVE: decimal_constants.ACTIVE})
            if user_object:
                raise AuthenticationFailed(response_messages.USER_LOGGED_IN)
            return True, None
        else:
            # Get Key from HTTP header
            token = get_token_from_request(request)

            if not token:
                raise AuthenticationFailed(response_messages.AUTHORIZATION_ERROR)

            session_object = get_data(model=AuthToken, filters={'token': token})
            if not session_object:
                raise AuthenticationFailed(response_messages.USER_NOT_LOGGED_IN)

            difference = timezone.now() - session_object.first().created_at
            if difference.seconds > SESSION_LENGTH:
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
    session_object.delete()

    return status


def get_token_from_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if 'key' in request.data:
        token = request.data['key']
    elif 'key' in request.GET:
        token = request.GET['key']
    return token if token else None
