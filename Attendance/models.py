from django.db.models import TimeField, IntegerField
from base.base_models import CreatedMixing, UserMixing, UpdatedMixing


class AttendanceMaster(CreatedMixing, UserMixing, UpdatedMixing):
    punchIn = TimeField(null=True)
    punchOut = TimeField(null=True)
    day = IntegerField()
    month = IntegerField()
    year = IntegerField()

    class Meta:
        db_table = 'attendance_master'
