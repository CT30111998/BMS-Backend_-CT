from django.db.models import CharField, ImageField, IntegerField, ForeignKey, CASCADE
import datetime
import os
from base.base_models import CreatedMixing, UpdatedMixing, DeletedMixing


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class BlogMaster(CreatedMixing, UpdatedMixing, DeletedMixing):
    postTitle = CharField(max_length=50, null=True)
    postImage = ImageField(upload_to=get_file_path, null=True)
    postDescription = CharField(max_length=255, null=True)

    def __str__(self):
        return self.postTitle

    class Meta:
        db_table = 'blog_master'


class Like(CreatedMixing):
    blog = ForeignKey(BlogMaster, on_delete=CASCADE, related_name="like_related_blog")
    like = IntegerField(default=0)

    class Meta:
        db_table = 'like_master'


class Comment(CreatedMixing):
    blog = ForeignKey(BlogMaster, on_delete=CASCADE, related_name="comment_related_blog")
    comment = CharField(max_length=255)

    class Meta:
        db_table = 'comment_master'
