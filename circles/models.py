from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from django.db import models, IntegrityError


class Circle(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    serial      = models.CharField(max_length=32, default=get_random_string(length=32), null=False, blank=False)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    requested   = models.ManyToManyField("user.Account", blank=True, related_name="requested", through="CircleRequests")
    members     = models.ManyToManyField("user.Account", blank=True, related_name="members", through="CircleMembership")
    connected   = models.ManyToManyField("user.Account", blank=True, related_name="connected")
    description = models.TextField(max_length=512, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.founder.username}"

    @property
    def has_description(self):
        return False if not bool(self.description) else True

    def browse(self):
        return reverse("circle:browse")

    def close(self):
        return reverse("circle:close")
            
    def open(self):
        return reverse("circle:open", args=[str(self.serial)])

    def link(self):
        return str(reverse("circle:link", args=[str(self.serial)]))

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
    
    class Meta:
        unique_together = ('founder', 'name')


class CircleRequests(models.Model):

    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    circle    = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} requested to join {self.circle.name}."

class CircleMembership(models.Model):

    user      = models.ForeignKey('user.Account', on_delete=models.CASCADE)
    circle    = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} approved."