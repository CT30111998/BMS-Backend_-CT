from rest_framework.serializers import ModelSerializer, IntegerField, CharField
from Auth.serializers import AuthUserSerializer
from .models import BlogMaster, BlogLike as LikeModel, BlogComment as CommentModel
from BMSystem.model_fields import (ID, BLOG_TITLE, BLOG_IMAGE, BLOG_DESC, CREATED_AT,
                                   CREATED_BY, UPDATED_AT, UPDATED_BY, LIKE, COMMENT)


class LikeSerializer(ModelSerializer):
    created_by = AuthUserSerializer(many=False)
    like = IntegerField(required=True)

    class Meta:
        model = LikeModel
        fields = (LIKE, CREATED_BY)


class CommentSerializer(ModelSerializer):
    created_by = AuthUserSerializer(many=False)
    comment = CharField(required=True)

    class Meta:
        model = CommentModel
        fields = (COMMENT, CREATED_BY)


class BlogSerializer(ModelSerializer):
    created_by = AuthUserSerializer(many=False)
    blog_like = LikeSerializer(many=True, read_only=True)
    blog_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogMaster
        fields = (ID, BLOG_TITLE, BLOG_IMAGE, BLOG_DESC, CREATED_AT, CREATED_BY, 'blog_like', 'blog_comment')
