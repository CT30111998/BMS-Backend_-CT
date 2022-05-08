import email
from django.db import models
from BMSystem import constants
from Auth.models import GroupMaster
from base.base_models import UserMixing, CreatedMixing, UpdatedMixing
import datetime
import os


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class UserMaster(UserMixing):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    mNo = models.IntegerField()
    email = models.EmailField()
    image = models.ImageField(upload_to=get_file_path, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    about = models.CharField(max_length=255, null=True)
    birthDate = models.DateField(null=True)
    dateOfJoining = models.DateField(null=True)
    jonTittle = models.CharField(max_length=50, null=True)
    updatedAt = models.DateField(null=True)
    createdAt = models.DateField()

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = 'user_master'


class DepartmentMaster(CreatedMixing, UpdatedMixing):
    dept = models.CharField(max_length=30)

    def __str__(self):
        return self.dept

    class Meta:
        db_table = 'department_master'


class ShiftMaster(CreatedMixing, UpdatedMixing):
    shift = models.CharField(max_length=50)

    def __str__(self):
        return self.shift

    class Meta:
        db_table = 'shift_master'


class UserGroup(UserMixing, CreatedMixing, UpdatedMixing):
    group = models.ForeignKey(
        GroupMaster,
        on_delete=models.CASCADE,
        related_name="related_user_group_group_master",
        verbose_name="User add in user group"
    )

    class Meta:
        db_table = "user_group"
