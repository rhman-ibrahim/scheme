from django.db import models


class Circle(models.Model):

    name        = models.CharField(max_length=32, null=False, blank=False)
    founder     = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="founder", null=False, blank=False)
    members     = models.ManyToManyField("user.Account", related_name="members", null=True, blank=True)
    connected   = models.ManyToManyField("user.Account",  null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)