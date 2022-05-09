from Auth.models import AuthMaster as AuthUser
from django.db.models import ForeignKey, Model, DateTimeField, CASCADE, IntegerField
from BMSystem import decimal_constants


class CreatedMixing(Model):
    created_by = ForeignKey(
        AuthUser,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_created_by"
    )
    created_at = DateTimeField()

    class Meta:
        abstract = True


class UpdatedMixing(Model):
    updated_by = ForeignKey(
        AuthUser,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_modified_by",
        null=True
    )
    updated_at = DateTimeField(null=True)

    class Meta:
        abstract = True


class UserMixing(Model):
    user = ForeignKey(
        AuthUser,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_auth_master"
    )

    class Meta:
        abstract = True


class DeletedMixing(Model):
    is_deleted = IntegerField(default=decimal_constants.NOT_DELETED)

    class Meta:
        abstract = True
