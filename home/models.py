from django.db import models
from django.utils import timezone

class TimeStamp(models.Model):
    
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Widget(TimeStamp):

    view = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    note = models.CharField(max_length=32)
    card = models.TextField(max_length=256)

    def __str__(self):
        return f"{self.view}'s {self.note}"