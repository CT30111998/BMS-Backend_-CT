from django.db.models import Model, EmailField, CharField, IntegerField, DateTimeField, ForeignKey, CASCADE
from BMSystem import decimal_constants
from base.query_modules import save_data


class AuthMaster(Model):
    email = EmailField(max_length=255)
    password = CharField(max_length=800)
    firstName = CharField(max_length=100)
    lastName = CharField(max_length=100)
    is_active = IntegerField(default=decimal_constants.NOT_ACTIVE)
    last_login = DateTimeField(null=True)
    is_deleted = IntegerField(default=decimal_constants.NOT_DELETED)

    class Meta:
        db_table = "auth_master"


class GroupMaster(Model):
    group_name = CharField(max_length=255)
    permission = IntegerField()

    class Meta:
        db_table = 'group_master'


def insert_group_data(apps, schema_editor):
    group_master = apps.get_model('Auth', 'GroupMaster')

    params = [
        {'group_name': 'Owner', 'permission': 1},
        {'group_name': 'Admin', 'permission': 2},
        {'group_name': 'Co-Admin', 'permission': 3},
        {'group_name': 'User', 'permission': 4}
    ]
    for param in params:
        save_group = save_data(model=group_master, fields=param)


class AuthToken(Model):
    token = CharField(max_length=800)
    user_master = ForeignKey(
        AuthMaster, related_name='auth_token_user', on_delete=CASCADE
    )
    created_at = DateTimeField()

    class Meta:
        db_table = 'bms_auth_session'
