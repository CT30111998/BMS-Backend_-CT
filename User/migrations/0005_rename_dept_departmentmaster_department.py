# Generated by Django 4.0.3 on 2022-05-11 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_usermaster_is_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departmentmaster',
            old_name='dept',
            new_name='department',
        ),
    ]
