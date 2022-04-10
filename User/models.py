import email
from django.db import models
from django.contrib.auth import models as auth_model
import datetime
import os


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class PositionMaster(models.Model):
    positionName = models.CharField(max_length=50)

    def __str__(self):
        return self.positionName


class UserGroup(models):
    groupName = models.CharField(max_length=50)

    def __str__(self):
        return self.groupName

class DepartmentMaster(models.Model):
    dept = models.CharField(max_length=30)

    def __str__(self):
        return self.dept


class WorkTypeMaster(models.Model):
    workType = models.CharField(max_length=50)

    def __str__(self):
        return self.workType


class JobTypeMaster(models.Model):
    jobType = models.CharField(max_length=50)

    def __str__(self):
        return self.jobType


class ShiftMaster(models.Model):
    shift = models.CharField(max_length=50)

    def __str__(self):
        return self.shift


class RoleMaster(models.Model):
    role = models.IntegerField()

    def __str__(self):
        return f'{self.role}'


class UserMaster(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(auth_model.User, on_delete=models.CASCADE)
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
    updatedAt = models.DateField(null=True)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class UserPosition(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    position = models.ForeignKey(PositionMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'
