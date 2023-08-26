# URLS
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    message  = models.TextField(max_length=256, blank=True, null=True, default="Sender did not provide a message.")
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f'from {self.sender} to {self.receiver} ({self.get_status_display()})'

    def validate_unique(self, exclude=None):
        if FriendRequest.objects.filter(
            Q(sender=self.receiver) & Q(receiver=self.sender),
            ~Q(status=0)
        ).exists():
            raise ValidationError('A friend request already exists between these users.')
        super(FriendRequest, self).validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FriendRequest, self).save(*args, **kwargs)
    
    @property
    def has_message(self):
        return False if not bool(self.message) else True
    
    def accept(self):
        self.status = 1
        self.receiver.profile.friends.add(self.sender)
        self.sender.profile.friends.add(self.receiver)
        self.receiver.save()
        self.sender.save()
        self.save()

    def reject(self):
        self.status = 0
        self.save()

    def cancel(self):
        self.delete()
        

class SpaceRequest(models.Model):

    message   = models.TextField(max_length=256, blank=True, null=True, default="Sender did not provide a message.")
    status    = models.IntegerField(default=2, choices=REQUEST_STATUS, blank=False,null=False)
    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    space     = models.ForeignKey('team.Space', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'from {self.user} to {self.space.name}/{self.space.founder} ({self.get_status_display()})'
    
    @property
    def has_message(self):
        return False if not bool(self.message) else True
    
    def accept(self):
        self.status = 1
        self.space.members.add(self.user)
        self.space.save()
        self.save()

    def reject(self):
        self.status = 0
        self.save()

    def cancel(self):
        self.delete()