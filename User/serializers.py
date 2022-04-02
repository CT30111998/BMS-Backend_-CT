from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from User.models import *
from BMSystem import constant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'
