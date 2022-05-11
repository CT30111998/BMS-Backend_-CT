from django.db.models import CharField
from base.base_models import CreatedMixing


class FeedbackMaster(CreatedMixing):
    feedback = CharField(max_length=800)

    class Meta:
        db_table = 'feedback_master'
