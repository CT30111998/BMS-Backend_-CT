# Generated by Django 4.0.3 on 2022-04-19 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Work', '0002_categorymaser_alter_groupmaster_created_by_usergroup_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='attendancemaster',
            table='attendance_master',
        ),
        migrations.AlterModelTable(
            name='categorymaser',
            table='category_master',
        ),
        migrations.AlterModelTable(
            name='groupmaster',
            table='group_master',
        ),
        migrations.AlterModelTable(
            name='usercategory',
            table='user_category',
        ),
        migrations.AlterModelTable(
            name='usergroup',
            table='user_group',
        ),
    ]
