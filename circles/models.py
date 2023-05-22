from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils import timezone


class Circle(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", related_name="members", blank=True)
    connected   = models.ManyToManyField("user.Account", blank=True)
    description = models.TextField(max_length=512, blank=True)


class Invitation(models.Model):

    limit    = models.IntegerField(null=False, blank=False, default=1)
    invitees = models.ManyToManyField("user.Account", blank=True)
    circle   = models.ForeignKey("circles.Circle", on_delete=models.CASCADE, null=False, blank=False)
    uuid     = models.CharField(max_length=32, default=get_random_string(length=32), null=False, blank=False)
    expired  = models.DateTimeField(default=(timezone.now() + timezone.timedelta(minutes=4)), null=False, blank=False)
    created  = models.DateTimeField(auto_now_add=True)