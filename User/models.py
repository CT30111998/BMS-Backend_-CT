import email
from django.db import models
import datetime
import os


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class Position(models.Model):
    positionName = models.CharField(max_length=50)


class Department(models.Model):
    dept = models.CharField(max_length=30)


class WorkType(models.Model):
    workType = models.CharField(max_length=50)


class JobType(models.Model):
    jobType = models.CharField(max_length=50)


class Shift(models.Model):
    shift = models.CharField(max_length=50)


class Role(models.Model):
    role = models.CharField(max_length=30)


class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    mNo = models.IntegerField()
    email = models.EmailField()
    image = models.ImageField(upload_to=get_file_path, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    empNo = models.IntegerField()
    about = models.CharField(max_length=255, null=True)
    birthDate = models.DateField(null=True)
    dateOfJoining = models.DateField(null=True)
    jonTittle = models.CharField(max_length=50, null=True)
    position = models.ForeignKey(Position, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    workTye = models.ForeignKey(WorkType, null=True, on_delete=models.CASCADE)
    jobType = models.ForeignKey(JobType, null=True, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, null=True, on_delete=models.CASCADE)
    role = models.IntegerField(default=2)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.email}"

