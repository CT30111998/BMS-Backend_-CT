# Generated by Django 4.0.3 on 2022-04-20 05:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Work', '0008_remove_attendancemaster_date_attendancemaster_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancemaster',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
