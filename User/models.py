from django.db.models import CharField, IntegerField, EmailField, ForeignKey, DateTimeField, \
    DateField, ImageField, CASCADE, BigIntegerField
from Auth.models import GroupMaster
from Department.models import DepartmentMaster
from base.base_models import UserMixing, CreatedMixing, UpdatedMixing, DeletedMixing
import datetime
import os


def get_file_path(request, filename):
    filename = "%s%s" % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S'), filename)
    return os.path.join('uploads/', filename)


class UserMaster(UserMixing, UpdatedMixing, DeletedMixing):
    firstName = CharField(max_length=100)
    lastName = CharField(max_length=100)
    mNo = BigIntegerField()
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
    department = ForeignKey(DepartmentMaster, related_name="user_departments", on_delete=CASCADE, null=True)

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = 'user_master'


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
