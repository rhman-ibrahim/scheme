from django.contrib import admin
from .models import Signal, Post, Comment

admin.site.register(Signal)
admin.site.register(Post)
admin.site.register(Comment)