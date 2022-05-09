from django.db.models import CharField, IntegerField, EmailField, ForeignKey, DateTimeField, \
    DateField, ImageField, CASCADE
from Auth.models import GroupMaster
from base.base_models import UserMixing, CreatedMixing, UpdatedMixing
import datetime
import os


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class UserMaster(UserMixing, UpdatedMixing):
    firstName = CharField(max_length=100)
    lastName = CharField(max_length=100)
    mNo = IntegerField()
    email = EmailField()
    image = ImageField(upload_to=get_file_path, null=True)
    address = CharField(max_length=250, null=True)
    city = CharField(max_length=50, null=True)
    state = CharField(max_length=50, null=True)
    country = CharField(max_length=50, null=True)
    about = CharField(max_length=255, null=True)
    birthDate = DateField(null=True)
    dateOfJoining = DateField(null=True)
    jonTittle = CharField(max_length=50, null=True)
    created_at = DateTimeField()

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = 'user_master'


class DepartmentMaster(CreatedMixing, UpdatedMixing):
    dept = CharField(max_length=30)

    def __str__(self):
        return self.dept

    class Meta:
        db_table = 'department_master'


class ShiftMaster(CreatedMixing, UpdatedMixing):
    shift = CharField(max_length=50)

    def __str__(self):
        return self.shift

    class Meta:
        db_table = 'shift_master'


class UserGroup(UserMixing, UpdatedMixing):
    group = ForeignKey(
        GroupMaster,
        on_delete=CASCADE,
        related_name="related_user_group_group_master",
        verbose_name="User add in user group"
    )
    created_at = DateTimeField()

    class Meta:
        db_table = "user_group"
