# DB
from django.db import models
from django.urls import reverse

# Helpers
from helpers.functions import generate_serial


REQUEST_STATUS = (
    (0, "Rejected"),
    (1, "Accepted"),
    (2, "Pending"),
)

class FriendRequest(models.Model):

    receiver = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="receiver")
    sender   = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="sender")
    serial   = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    status   = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def accept(self):
        return reverse("mate:accept_friend_request", args=[str(self.id)])

    def reject(self):
        return reverse("mate:reject_friend_request", args=[str(self.id)])

    def cancel(self):
        return reverse("mate:delete_friend_request", args=[str(self.id)])