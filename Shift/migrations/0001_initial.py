# Generated by Django 4.0.3 on 2022-05-12 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0002_authmaster_firstname_authmaster_lastname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True)),
                ('shift', models.CharField(max_length=30)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_created_by', to='Auth.authmaster')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related_modified_by', to='Auth.authmaster')),
            ],
            options={
                'db_table': 'shift_master',
            },
        ),
    ]
