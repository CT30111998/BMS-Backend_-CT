# Generated by Django 4.0.3 on 2022-05-07 14:38

from django.db import migrations, models
from base.query_modules import save_data
from Auth.models import insert_group_data


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=800)),
                ('is_active', models.IntegerField(default=0)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'auth_master',
            },
        ),
        migrations.CreateModel(
            name='GroupMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
                ('permission', models.IntegerField()),
            ],
            options={
                'db_table': 'group_master',
            },
        ),
        migrations.RunPython(insert_group_data),
    ]
