# Generated by Django 4.0.3 on 2022-04-20 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Work', '0009_attendancemaster_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancemaster',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
