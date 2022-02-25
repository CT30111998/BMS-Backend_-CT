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
    mNo = models.IntegerField(null=True)
    image = models.ImageField(upload_to=get_file_path, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    empNo = models.IntegerField()
    about = models.CharField(max_length=255, null=True)
    birthDate = models.DateField()
    dateOfJoining = models.DateField()
    jonTittle = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    workTye = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    jobType = models.ForeignKey(JobType, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)

