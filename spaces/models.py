from django.db import models
from django.core.validators import RegexValidator


ROOM_STATUS = (
    (0, "Opened"),
    (1, "Closed")
)

class Room(models.Model):

    circle  = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)
    space   = models.CharField(
        max_length = 36,
        validators = [
            RegexValidator(
                regex='^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
                message='this is not a valid room name.'
            )
        ],
        blank      = False,
        null       = False,
    )
    status         = models.IntegerField(choices=ROOM_STATUS, default=0, blank=False, null=False)

    def __str__(self):
        return self.space
    

class Message(models.Model):

    room    = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender  = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body    = models.TextField()

    def __str__(self):
        return f'sent by {self.sender} on {self.created} in {self.room.circle}'