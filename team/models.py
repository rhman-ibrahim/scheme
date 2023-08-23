# Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from django.urls import reverse

# Models
from django.db import models

# Helpers
from helpers.functions import generate_serial, secret

# Ping
from ping.models import Room


class Space(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    serial      = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    description = models.TextField(max_length=512, blank=True)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", blank=True, related_name="members", through="Membership")
    password    = models.CharField(max_length=128, null=False, blank=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    @property
    def has_description(self):
        return False if not bool(self.description) else True
    
    @property
    def join_requests(self):
        from mate.models import SpaceRequest
        return SpaceRequest.objects.filter(circle=self, status=2)

    @property
    def logs(self):
        return LogEntry.objects.filter(
            content_type = ContentType.objects.get_for_model(Space),
            object_id    = self.id
        )
    
    @property
    def room(self):
        return Room.objects.get(serial=self.serial)
    
    def founder_friends_queryset(self):
        from user.models import Account
        friends = [int(friend.id) for friend in self.founder.scheme.friends.all()]
        members = [int(member.id) for member in self.members.all()]
        return Account.objects.filter(
            pk__in=list(set(friends).symmetric_difference(set(members)))
        )
    
    
    def check_password(self, raw_password):
        return self.password == secret(raw_password)

    def user_role(self, user):
        if user in self.members.all():
            return "member"
        elif user == self.founder:
            return "founder"
        return None


    def __str__(self):
        return f"{self.name} by {self.founder.username}"    
    
    class Meta:
        unique_together = ('founder', 'name')


class Membership(models.Model):

    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    space     = models.ForeignKey('team.Space', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} approved."