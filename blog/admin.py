from django.contrib import admin
from .models import Blog, Comment, HashTag, Category
# Register your models here.

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(HashTag)
