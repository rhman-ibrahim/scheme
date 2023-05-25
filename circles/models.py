from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone


class Circle(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", related_name="members", blank=True)
    connected   = models.ManyToManyField("user.Account", blank=True)
    description = models.TextField(max_length=512, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} by {self.founder.username}"


class Invitation(models.Model):

    limit    = models.IntegerField(null=False, blank=False, default=1)
    invitees = models.ManyToManyField("user.Account", blank=True)
    circle   = models.ForeignKey("circles.Circle", on_delete=models.CASCADE, null=False, blank=False)
    uuid     = models.CharField(max_length=32, default=get_random_string(length=32), null=False, blank=False)
    expired  = models.DateTimeField(default=(timezone.now() + timezone.timedelta(minutes=4)), null=False, blank=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.circle.name} by {self.circle.founder.username}"