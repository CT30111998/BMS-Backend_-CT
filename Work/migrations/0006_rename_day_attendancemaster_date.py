# Generated by Django 4.0.3 on 2022-04-19 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Work', '0005_alter_attendancemaster_updated_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancemaster',
            old_name='day',
            new_name='date',
        ),
    ]
