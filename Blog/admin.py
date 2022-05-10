from django.contrib import admin
from .models import BlogMaster, BlogLike, BlogComment

admin.site.register(BlogMaster)
admin.site.register(BlogLike)
admin.site.register(BlogComment)
# Register your models here.
