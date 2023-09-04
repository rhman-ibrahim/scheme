from django.db import models
from django.utils import timezone

class TimeStamp(models.Model):
    
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True