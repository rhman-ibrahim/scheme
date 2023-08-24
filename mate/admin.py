from django.contrib import admin
from .models import FriendRequest, SpaceRequest


admin.site.register(FriendRequest)
admin.site.register(SpaceRequest)