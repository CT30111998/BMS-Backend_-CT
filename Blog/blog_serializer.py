from rest_framework import serializers
from .models import *


class BlogMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogMaster
        fields = '__all__'
