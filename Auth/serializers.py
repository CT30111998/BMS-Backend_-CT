from rest_framework.serializers import Serializer, CharField, EmailField, IntegerField, ValidationError, ModelSerializer
from BMSystem import constants, decimal_constants, response_messages
from base.common_helpers import check_email_format
from base.query_modules import get_data
from Auth.jwt_module import jwt_decode, jwt_encode
from Auth.models import AuthMaster


class CreateUserSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)
    firstName = CharField(required=True)
    lastName = CharField(required=True)
    confirm_password = CharField(required=True)
    is_active = IntegerField(default=decimal_constants.NOT_ACTIVE)
    is_deleted = IntegerField(default=decimal_constants.NOT_DELETED)

    def validate(self, data):
        error_dict = dict()

        check_email_valid = check_email_format(data['email'])
        if not check_email_valid:
            error_dict['email'] = response_messages.EMAIL_NOT_VALID

        user_object = get_data(model=AuthMaster, filters={'email': data['email']})
        if user_object:
            error_dict['user'] = response_messages.USER_EXIST

        if data['password'] != data['confirm_password']:
            error_dict['password'] = response_messages.PASSWORD_NOT_SAME

        if error_dict:
            raise ValidationError(error_dict)

        # Encrypt password
        data['password'] = jwt_encode({'password': data['password']})
        return data


class LoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)

    def validate(self, data):
        error_dict = dict()

        user_object = get_data(model=AuthMaster, filters={'email': data['email']})
        if not user_object:
            error_dict['other_errors'] = response_messages.USER_NOT_EXIST
        else:
            # Check user active status
            user = user_object.first()
            if user.is_active == decimal_constants.ACTIVE:
                error_dict['email'] = response_messages.USER_LOGGED_IN
            else:
                decoded_pass = jwt_decode(user.password)
                if data['password'] != decoded_pass['password']:
                    error_dict['password'] = response_messages.INCORRECT_PASSWORD

        if error_dict:
            raise ValidationError(error_dict)
        return data


class AuthUserSerializer(ModelSerializer):
    class Meta:
        model = AuthMaster
        fields = ('id', 'firstName', 'lastName')
