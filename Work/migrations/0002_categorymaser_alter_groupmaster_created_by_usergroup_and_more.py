# Generated by Django 4.0.3 on 2022-04-19 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Work', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryMaser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_category_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Category created by user name')),
            ],
        ),
        migrations.AlterField(
            model_name='groupmaster',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_group_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Group created by user name'),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_group_add_by', to=settings.AUTH_USER_MODEL, verbose_name='User add by in user group')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Work.groupmaster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_group_user_master', to=settings.AUTH_USER_MODEL, verbose_name='User add in user group')),
            ],
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_category_add_by', to=settings.AUTH_USER_MODEL, verbose_name='User add by in user category')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Work.categorymaser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_category_user_master', to=settings.AUTH_USER_MODEL, verbose_name='User add in user category')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punchIn', models.TimeField(null=True)),
                ('punchOut', models.TimeField(null=True)),
                ('day', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_attendance_user_master', to=settings.AUTH_USER_MODEL, verbose_name='User add in attendance')),
            ],
        ),
    ]