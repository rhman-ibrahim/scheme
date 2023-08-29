# Django
from django.urls import reverse
from django.db import models

# Helpers
from helpers.functions import generate_identifier


class Room(models.Model):

    identifier  = models.CharField(max_length=36, default=generate_identifier, null=False, blank=False)
    status      = models.BooleanField(default=True, blank=False, null=False)
    description = models.TextField(default="This room has no description.")
    members     = models.ManyToManyField("user.Account")

    def __str__(self):
        return self.identifier
    
    def update_status(self):
        return reverse("ping:update_room_status", args=[str(self.identifier)])
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    
    @property
    def conversation(self):
        return "group" if self.members.count() > 2 else "one-to-one"
    

class Message(models.Model):

    room    = models.ForeignKey("ping.Room", on_delete=models.CASCADE)
    sender  = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body    = models.TextField()

    def __str__(self):
        return f'sent by {self.sender} on {self.created} in {self.room.space}'