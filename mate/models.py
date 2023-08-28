# Validators
from django.core.exceptions import (
    ValidationError, MultipleObjectsReturned
)
# DB
from django.db.models import Q
from django.db import models

# Models
from ping.models import Room

# Helpers
from helpers.functions import generate_identifier


REQUEST_STATUS = (
    (0, "Rejected"),
    (1, "Accepted"),
    (2, "Pending"),
)

class FriendRequest(models.Model):

    status     = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    identifier = models.CharField(max_length=36, default=generate_identifier, null=False, blank=False)
    receiver   = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="receiver")
    sender     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="sender")
    message    = models.TextField(max_length=256, blank=True, null=True, default="Sender did not provide a message.")
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    @property
    def has_message(self):
        return False if not bool(self.message) else True
    
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
        
    def accept(self):
        self.status = 1
        self.receiver.profile.friends.add(self.sender.profile)
        self.receiver.save()
        self.save()
        self.build()

    def build(self):
        Friendship.objects.create(identifier=self.identifier).users.set([self.sender, self.receiver])
        Room.objects.create(identifier=self.identifier).members.set([self.sender, self.receiver])

    def reject(self):
        self.status = 0
        self.save()

    def cancel(self):
        self.delete()
        
class Friendship(models.Model):

    users      = models.ManyToManyField("user.Account", max_length=2, editable=False)
    identifier = models.CharField(max_length=36, default=generate_identifier, null=False, blank=False)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)


class SpaceSignal(models.Model):

    message   = models.TextField(max_length=256, blank=True, null=True, default="Sender did not provide a message.")
    status    = models.IntegerField(default=2, choices=REQUEST_STATUS, blank=False,null=False)
    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    space     = models.ForeignKey('team.Space', on_delete=models.CASCADE)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    class Meta:
        abstract        = True
        unique_together = ('user', 'space') 

    @property
    def has_message(self):
        return False if not bool(self.message) else True
    
    def accept(self):
        self.status = 1
        self.space.members.add(self.user)
        self.space.save()
        self.save()
        self.build()

    def build(self):
        Membership.objects.create(user=self.user, space=self)
        room, created = Room.objects.get_or_create(identifier=self.identifier)
        room.members.add(self.user)

    def reject(self):
        self.status = 0
        self.save()

    def cancel(self):
        self.delete()

class SpaceRequest(SpaceSignal):
    
    def __str__(self):
        return f'from {self.user} to {self.space.name}/{self.space.founder} ({self.get_status_display()})'

class SpaceInvitation(SpaceSignal):

    def __str__(self):
        return f'from {self.space.name}/{self.space.founder} to {self.user} ({self.get_status_display()})'
    
class Membership(models.Model):

    user    = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    space   = models.ForeignKey('team.Space', on_delete=models.CASCADE)
    key     = models.CharField(max_length=32, default=generate_identifier, null=False, blank=False)
    ready   = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'space')
    
    def __str__(self):
        return f"On {self.created.strftime('%B %d, %Y')}: {self.user.username} joined {self.space.name}."
    
    def save(self, *args, **kwargs):
        try:
            Membership.objects.get(key=self.key)
            self.ready = False
        except MultipleObjectsReturned:
            self.ready = True
        except Membership.DoesNotExist:
            pass
        super(Membership, self).save(*args, **kwargs)