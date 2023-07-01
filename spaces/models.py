from django.db import models
from django.utils.crypto import get_random_string


ROOM_STATUS = (
    (0, "Opened"),
    (1, "Closed")
)

class Room(models.Model):

    circle   = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)
    members  = models.ManyToManyField("user.Account")
    serial   = models.CharField(max_length=36, default=get_random_string(length=32), null=False, blank=False)
    status   = models.IntegerField(choices=ROOM_STATUS, default=0, blank=False, null=False)

    def __str__(self):
        return self.serial
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    

class Message(models.Model):

    room    = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender  = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body    = models.TextField()

    def __str__(self):
        return f'sent by {self.sender} on {self.created} in {self.room.circle}'