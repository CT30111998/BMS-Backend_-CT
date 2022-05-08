from django.db import models
from base.base_models import CreatedMixing, UserMixing, UpdatedMixing


class AttendanceMaster(CreatedMixing, UserMixing, UpdatedMixing):
    punchIn = models.TimeField(null=True)
    punchOut = models.TimeField(null=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_master'


class FeedbackMaster(CreatedMixing):
    feedback = models.CharField(max_length=800)
