from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from User.models import *
from BMSystem import constant


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['user_id'] = AuthUserSerializer(read_only=True)
    #     return super(UserSerializer, self).to_representation(instance)


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
