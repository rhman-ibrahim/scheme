# Models
from ping.models import Room

# Hlepers
from helpers.decorators import back

@back
def update_room_status(request, identifier):
    room = Room.objects.get(identifier=identifier)
    room.status = False if room.status else True
    room.save()