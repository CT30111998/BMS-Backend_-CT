from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.


class GroupMaster(models.Model):
    groupName = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        AuthUser,
        related_name="related_group_created_by",
        verbose_name="Group created by user name",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "group_master"


class UserGroup(models.Model):
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name="related_user_group_user_master",
        verbose_name="User add in user group"
    )
    group = models.ForeignKey(GroupMaster, on_delete=models.CASCADE)
    add_by = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name="related_user_group_add_by",
        verbose_name="User add by in user group"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_group"


class CategoryMaser(models.Model):
    categoryName = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        AuthUser,
        related_name="related_category_created_by",
        verbose_name="Category created by user name",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "category_master"


class UserCategory(models.Model):
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name="related_user_category_user_master",
        verbose_name="User add in user category"
    )
    category = models.ForeignKey(CategoryMaser, on_delete=models.CASCADE)
    add_by = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name="related_user_category_add_by",
        verbose_name="User add by in user category"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_category'


class AttendanceMaster(models.Model):
    punchIn = models.TimeField(null=True)
    punchOut = models.TimeField(null=True)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name="related_user_attendance_user_master",
        verbose_name="User add in attendance"
    )
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        AuthUser,
        related_name="related_attendance_created_by",
        verbose_name="Attendance created by user name",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        AuthUser,
        related_name="related_attendance_updated_by",
        verbose_name="Attendance updated by user name",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = 'attendance_master'
