# Django
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.utils import timezone

# Models
from django.db import models
from user.models import Account

# Helpers
from helpers.functions import generate_serial, secret

# Ping
from ping.models import Room



REQUEST_STATUS = (
    (0, "Rejected"),
    (1, "Accepted"),
    (2, "Pending"),
)

class Circle(models.Model):

    # Identify
    name        = models.CharField(max_length=32, null=False, blank=False)
    serial      = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    description = models.TextField(max_length=512, blank=True)
    # Users
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", blank=True, related_name="members", through="CircleMembership")
    # Password
    password    = models.CharField(max_length=128, null=False, blank=False)
    # Time
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    @property
    def has_description(self):
        return False if not bool(self.description) else True
    
    @property
    def join_requests(self):
        return CircleRequest.objects.filter(circle=self, status=2)

    @property
    def logs(self):
        return LogEntry.objects.filter(
            content_type = ContentType.objects.get_for_model(Circle),
            object_id    = self.id
        )
    
    @property
    def room(self):
        return Room.objects.get(serial=self.serial)
    
    def founder_friends_queryset(self):
        friends = [int(friend.id) for friend in self.founder.scheme.friends.all()]
        members = [int(member.id) for member in self.members.all()]
        return Account.objects.filter(
            pk__in=list(set(friends).symmetric_difference(set(members)))
        )
    
    
    def check_password(self, raw_password):
        return self.password == secret(raw_password)

    def user_role(self, user):
        if user in self.members.all(): return "member"
        elif user == self.founder: return "founder"
        return None


    def __str__(self):
        return f"{self.name} by {self.founder.username}"    
    
    class Meta:
        unique_together = ('founder', 'name')


class CircleRequest(models.Model):

    status    = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    circle    = models.ForeignKey('team.Circle', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} requested to join {self.circle.name}."


class CircleMembership(models.Model):

    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    circle    = models.ForeignKey('team.Circle', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} approved."