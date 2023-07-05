# Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from django.urls import reverse
from django.db import models
# Spaces
from spaces.models import Room
# Helpers
from helpers.functions import generate_serial

class Circle(models.Model):

    # Identify
    name        = models.CharField(max_length=32, null=False, blank=False)
    serial      = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    description = models.TextField(max_length=512, blank=True)
    # Users
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    requested   = models.ManyToManyField("user.Account", blank=True, related_name="requested", through="CircleRequests")
    members     = models.ManyToManyField("user.Account", blank=True, related_name="members", through="CircleMembership")
    # Time
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.founder.username}"

    @property
    def has_description(self):
        return False if not bool(self.description) else True

    def browse(self):
        return reverse("team:browse")

    def close(self):
        return reverse("team:close")
            
    def open(self):
        return reverse("team:open", args=[str(self.serial)])

    def link(self):
        return str(reverse("team:link", args=[str(self.serial)]))

    def logs(self):
        return LogEntry.objects.filter(
            content_type = ContentType.objects.get_for_model(Circle),
            object_id    = self.id
        )
    
    def user_role(self, user):
        if user in self.members.all():
            return "member"
        elif user == self.founder:
            return "founder"
        return None
    
    @property
    def room_members_synced(self):
        room           = Room.objects.get(serial=self.serial)
        circle_members = [member.id for member in self.members.all()]
        circle_members.append(self.founder.id)
        if set(circle_members) == set([member.id for member in room.members.all()]):
            return True
        return False
    
    class Meta:
        unique_together = ('founder', 'name')


class CircleRequests(models.Model):

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