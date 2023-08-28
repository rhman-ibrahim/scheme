from django.contrib import admin
from .models import (
    FriendRequest, Friendship,
    SpaceRequest, SpaceInvitation, Membership
)


admin.site.register(FriendRequest)
admin.site.register(SpaceRequest)
admin.site.register(SpaceInvitation)
admin.site.register(Friendship)
admin.site.register(Membership)