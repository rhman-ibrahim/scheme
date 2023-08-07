# Django
from django.contrib import messages
from django.shortcuts import redirect

# Models
from ping.models import Room

# Hlepers
from helpers.decorators import back

@back
def update_room_status(request, serial):
    query = Room.objects.filter(serial=serial)
    if query.exists() and query.count() == 1:
        room        = query.first()
        room.status = False if room.status else True
        room.save()
    else:
        messages.warning(request, "something has gone wrong")