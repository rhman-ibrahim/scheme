from django.db import models
from helpers.functions import generate_serial
from django.core.exceptions import MultipleObjectsReturned


class Token(models.Model):

    user    = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    key     = models.CharField(max_length=32, default=generate_serial, null=False, blank=False)
    ready   = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        try:
            Token.objects.get(key=self.key)
            self.ready = False
        except MultipleObjectsReturned:
            self.ready = True
        except Token.DoesNotExist:
            pass
        super(Token, self).save(*args, **kwargs)


class Secret(models.Model):

    user    = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    space   = models.ForeignKey("team.Space", on_delete=models.CASCADE)
    key     = models.CharField(max_length=32, default=generate_serial, null=False, blank=False)
    ready   = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'space')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        try:
            Secret.objects.get(key=self.key)
            self.ready = False
        except MultipleObjectsReturned:
            self.ready = True
        except Secret.DoesNotExist:
            pass
        super(Secret, self).save(*args, **kwargs)