from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User as AuthUser
from User.models import UserMaster, DepartmentMaster
from BMSystem.model_fields import ID, DEPARTMENT, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY
from BMSystem import constants


class AuthUserSerializer(ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserMaster
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = DepartmentMaster
        fields = (ID, DEPARTMENT, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY)

# class UserPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPermission
#         fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['user_id'] = AuthUserSerializer(read_only=True)
    #     return super(UserSerializer, self).to_representation(instance)


