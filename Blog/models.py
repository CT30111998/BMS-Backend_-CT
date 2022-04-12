from django.db import models
import datetime
import os
from django.contrib.auth.models import User as AuthUser
from User import models as um


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class Blog(models.Model):
    timeStamp = models.TimeField(auto_now_add=True)
    blogTittle = models.CharField(max_length=50)
    postImage = models.ImageField(upload_to=get_file_path, null=True)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.blogTittle


class Like(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    likedAt = models.DateField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    createdAt = models.DateField(auto_now_add=True)
