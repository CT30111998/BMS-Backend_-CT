from django.db.models import CharField, CASCADE, ForeignKey
from base.base_models import CreatedMixing, UpdatedMixing, DeletedMixing, UserMixing


class DepartmentMaster(CreatedMixing, UpdatedMixing):
    department = CharField(max_length=30)

    def __str__(self):
        return self.department

    class Meta:
        db_table = 'department_master'


class UserDepartment(CreatedMixing, UpdatedMixing, UserMixing):
    department = ForeignKey(DepartmentMaster, on_delete=CASCADE, related_name='user_department')
