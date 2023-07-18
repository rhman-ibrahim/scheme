# DB
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models

# Helpers
from helpers.functions import generate_serial


REQUEST_STATUS = (
    (0, "Rejected"),
    (1, "Accepted"),
    (2, "Pending"),
)

class FriendRequest(models.Model):

    status   = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    serial   = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    receiver = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="receiver")
    sender   = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="sender")
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def accept(self):
        return reverse("mate:accept_friend_request", args=[str(self.id)])

    def reject(self):
        return reverse("mate:reject_friend_request", args=[str(self.id)])

    def cancel(self):
        return reverse("mate:delete_friend_request", args=[str(self.id)])
    
    def validate_unique(self, exclude=None):
        # Check if there is an existing friend request with the sender and receiver fields swapped
        if FriendRequest.objects.filter(sender=self.receiver, receiver=self.sender).exists():
            raise ValidationError('A friend request already exists between these users.')
        # Call the parent validate_unique method to check for any other unique constraints
        super(FriendRequest, self).validate_unique(exclude=exclude)
    
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FriendRequest, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('sender', 'receiver')