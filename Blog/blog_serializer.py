from rest_framework import serializers
from .models import *


class BlogMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
