from django.contrib.auth.models import User as AuthUser
from django.db.models import ForeignKey, Model, DateTimeField, CASCADE


class CreatedMixing(Model):
    created_by = ForeignKey(AuthUser, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_related_created_by")
    created_at = DateTimeField()

    class Meta:
        abstract = True


class UpdatedMixing(Model):
    updated_by = ForeignKey(AuthUser, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_related_modified_by")
    updated_at = DateTimeField(null=True)

    class Meta:
        abstract = True


class UserMixing(Model):
    user = ForeignKey(AuthUser, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_related_user")

    class Meta:
        abstract = True
