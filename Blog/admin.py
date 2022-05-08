from django.contrib import admin
from .models import BlogMaster, Like, Comment

admin.site.register(BlogMaster)
admin.site.register(Like)
admin.site.register(Comment)
# Register your models here.
