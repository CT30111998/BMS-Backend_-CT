from django.db.models import CharField, ImageField, IntegerField, ForeignKey, CASCADE
import datetime
import os
from base.base_models import CreatedMixing, UpdatedMixing, DeletedMixing


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class BlogMaster(CreatedMixing, DeletedMixing):
    postTitle = CharField(max_length=50, null=True)
    postImage = ImageField(upload_to=get_file_path, null=True)
    postDescription = CharField(max_length=255, null=True)

    def __str__(self):
        return self.postTitle

    class Meta:
        db_table = 'blog_master'


class BlogLike(CreatedMixing):
    blog = ForeignKey(BlogMaster, on_delete=CASCADE, related_name="blog_like")
    like = IntegerField(default=0)

    class Meta:
        db_table = 'blog_like'


class BlogComment(CreatedMixing):
    blog = ForeignKey(BlogMaster, on_delete=CASCADE, related_name="blog_comment")
    comment = CharField(max_length=255)

    class Meta:
        db_table = 'blog_comment'
