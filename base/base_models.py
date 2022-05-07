from django.contrib.auth.models import User as AuthUser
from django.db.models import ForeignKey, Model, DateTimeField, CASCADE


class CreatedMixer(Model):
    created_by = ForeignKey(AuthUser, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_related_created_by")
    created_time = DateTimeField()

    class Meta:
        abstract = True
