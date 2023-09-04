from django.contrib import admin
from .models import (
    FriendRequest, Friendship,
    SpaceRequest, SpaceInvitation
)


admin.site.register(FriendRequest)
admin.site.register(SpaceRequest)
admin.site.register(SpaceInvitation)
admin.site.register(Friendship)