from django.db import models
import datetime
import os
from django.contrib.auth.models import User as AuthUser
from User import models as um


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class Master(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    blogTitle = models.CharField(max_length=50, null=True)
    postImage = models.ImageField(upload_to=get_file_path, null=True)
    description = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.blogTitle


class Like(models.Model):
    like_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Master, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    liked_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Master, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
