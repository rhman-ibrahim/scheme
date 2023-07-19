# Django
from django.db import models
# Helpers
from helpers.functions import generate_serial


ROOM_STATUS = (
    (0, "Opened"),
    (1, "Closed")
)

class Room(models.Model):

    serial   = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    status   = models.IntegerField(choices=ROOM_STATUS, default=0, blank=False, null=False)
    members  = models.ManyToManyField("user.Account")

    def __str__(self):
        return self.serial
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    
    @property
    def conversation(self):
        return "group" if self.members.count() > 2 else "one-to-one"
    

class Message(models.Model):

    room    = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender  = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body    = models.TextField()

    def __str__(self):
        return f'sent by {self.sender} on {self.created} in {self.room.circle}'