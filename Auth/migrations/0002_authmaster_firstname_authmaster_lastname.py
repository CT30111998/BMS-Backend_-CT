# Generated by Django 4.0.3 on 2022-05-10 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authmaster',
            name='firstName',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='authmaster',
            name='lastName',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
