from dataclasses import fields
from rest_framework import serializers
from User.models import *
from BMSystem import constant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstName')