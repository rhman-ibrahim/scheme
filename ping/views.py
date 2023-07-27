# Django
from django.shortcuts import redirect
from django.contrib import messages

# Models
from ping.models import Room


def update_room_status(request, serial):
    query = Room.objects.filter(serial=serial)
    if query.exists() and query.count() == 1:
        room        = query.first()
        room.status = False if room.status else True
        room.save()
        return redirect("user:back")
    else:
        messages.warning(request, "something has gone wrong")
    return redirect("user:back")