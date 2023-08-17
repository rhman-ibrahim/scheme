# Django
from django.contrib import messages

# Models
from ping.models import Room

# Hlepers
from helpers.decorators import back

@back
def update_room_status(request, serial):
    room = Room.objects.get(serial=serial)
    room.status = False if room.status else True
    room.save()