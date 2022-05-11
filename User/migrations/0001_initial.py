# Generated by Django 4.0.3 on 2022-05-11 12:36

import User.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0002_authmaster_firstname_authmaster_lastname'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(null=True)),
                ('is_deleted', models.IntegerField(default=0)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('mNo', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(null=True, upload_to=User.models.get_file_path)),
                ('address', models.CharField(max_length=250, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('about', models.CharField(max_length=255, null=True)),
                ('birthDate', models.DateField(null=True)),
                ('dateOfJoining', models.DateField(null=True)),
                ('jonTittle', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_modified_by', to='Auth.authmaster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_auth_master', to='Auth.authmaster')),
            ],
            options={
                'db_table': 'user_master',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_group_group_master', to='Auth.groupmaster', verbose_name='User add in user group')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_modified_by', to='Auth.authmaster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_auth_master', to='Auth.authmaster')),
            ],
            options={
                'db_table': 'user_group',
            },
        ),
        migrations.CreateModel(
            name='ShiftMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True)),
                ('shift', models.CharField(max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_created_by', to='Auth.authmaster')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_modified_by', to='Auth.authmaster')),
            ],
            options={
                'db_table': 'shift_master',
            },
        ),
    ]
