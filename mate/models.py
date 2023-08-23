# URLS
from django.urls import reverse
from django.utils import timezone

# Validators
from django.core.exceptions import ValidationError

# DB
from django.db.models import Q
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
        return reverse("mate:accept_request", args=[str(self.id)])

    def reject(self):
        return reverse("mate:reject_request", args=[str(self.id)])

    def cancel(self):
        return reverse("mate:delete_request", args=[str(self.id)])
    
    def validate_unique(self, exclude=None):
        if FriendRequest.objects.filter(Q(sender=self.receiver) & Q(receiver=self.sender), ~Q(status=0)).exists():
            raise ValidationError('A friend request already exists between these users.')
        super(FriendRequest, self).validate_unique(exclude=exclude)
    
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FriendRequest, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('sender', 'receiver')


class SpaceRequest(models.Model):

    status    = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    space     = models.ForeignKey('team.Space', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} requested to join {self.space.name}."
    
    def cancel(self):
        return reverse("team:delete_request", args=[str(self.id)])