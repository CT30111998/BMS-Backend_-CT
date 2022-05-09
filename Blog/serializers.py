from rest_framework.serializers import ModelSerializer
from Auth.serializers import AuthUserSerializer
from .models import BlogMaster, Like, Comment
from BMSystem.model_fields import (ID, BLOG_TITLE, BLOG_IMAGE, BLOG_DESC, CREATED_AT,
                                   CREATED_BY, UPDATED_AT, UPDATED_BY)


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ()


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment


class BlogSerializer(ModelSerializer):
    created_by = AuthUserSerializer
    updated_by = AuthUserSerializer

    class Meta:
        model = BlogMaster
        fields = (ID, BLOG_TITLE, BLOG_IMAGE, BLOG_DESC, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY)
