from django.contrib import admin
from .models import Scheme, Profile, FriendRequest


admin.site.register(Scheme)
admin.site.register(Profile)
admin.site.register(FriendRequest)