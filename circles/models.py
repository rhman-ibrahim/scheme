from django.db import models


STATUS_CHOICES = (
    (0, "Pending"),
    (1, "Opened"),
    (2, "Closed")
)

RESULT_CHOICES = (
    (0, "Pending"),
    (1, "Accepted"),
    (2, "Rejected"),
)


class Circle(models.Model):

    name        = models.CharField(max_length=50, blank=False, null=False)
    founder     = models.ForeignKey("user.Account", related_name="founder", on_delete=models.CASCADE)
    members     = models.ManyToManyField("user.Account", related_name="members", blank=True)
    description = models.TextField(max_length=512, blank=False, null=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)


class Connection(models.Model):

    followee  = models.OneToOneField("user.Account", related_name="followee", on_delete=models.CASCADE)
    followers = models.ManyToManyField("user.Account", related_name="followers")

    def __str__(self):
        return f"{self.followee.username}'s followers" 
    

class joinRequest(models.Model):

    sender   = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    circle   = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)
    status   = models.IntegerField(choices=STATUS_CHOICES, default=0, blank=False, null=False)
    result   = models.IntegerField(choices=RESULT_CHOICES, default=0, blank=False, null=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)


class followRequest(models.Model):

    sender   = models.ForeignKey("user.Account", related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey("user.Account", related_name="receiver", on_delete=models.CASCADE)
    status   = models.IntegerField(choices=STATUS_CHOICES, default=0, blank=False, null=False)
    result   = models.IntegerField(choices=RESULT_CHOICES, default=0, blank=False, null=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'From {self.sender.username} To {self.receiver.username} ({STATUS_CHOICES[self.status][1]})'
    
    class Meta:
        unique_together = ('sender', 'receiver',)