# Generated by Django 4.0.3 on 2022-04-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_rename_blog_comment_blog_rename_blog_like_blog_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]