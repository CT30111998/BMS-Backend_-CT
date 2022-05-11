from django.db.models import CharField, CASCADE
from base.base_models import CreatedMixing, UpdatedMixing, DeletedMixing


class DepartmentMaster(CreatedMixing, UpdatedMixing):
    department = CharField(max_length=30)

    def __str__(self):
        return self.department

    class Meta:
        db_table = 'department_master'
