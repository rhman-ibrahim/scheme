# Django
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.admin.models import LogEntry
from django.db import models

# Models
from ping.models import Room

# Helpers
from helpers.functions import generate_identifier, secret


class Space(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    identifier  = models.CharField(max_length=32, default=generate_identifier, null=False, blank=False)
    description = models.TextField(max_length=512, blank=True)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", blank=True, related_name="members", through="Membership")
    password    = models.CharField(max_length=128, null=False, blank=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('founder', 'name')
    
    def __str__(self):
        return f"{self.name} by {self.founder.username}"
    
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
        return Room.objects.get(identifier=self.identifier)
    
    def founder_friends_queryset(self):
        from user.models import Account
        friends = [int(friend.id) for friend in self.founder.profile.friends.all()]
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