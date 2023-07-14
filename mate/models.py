# Django
from django.db.models import Q
from django.contrib.admin.models import LogEntry
from django.core.validators import FileExtensionValidator
from django.contrib.admin.models import LogEntry
from django.db import models
# Helpers
from helpers.functions import completion, profile_picture_path_handler
# Circles
from team.models import Circle


class Profile(models.Model):
    
    user    = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    name    = models.CharField(max_length=64, blank=True, null=True)
    email   = models.EmailField(max_length=256, unique=True, blank=True, null=True)
    about   = models.TextField(max_length=256, blank=True, null=True)
    picture = models.ImageField(
        default='user/profile/default.jpg',
        upload_to=profile_picture_path_handler,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg","jpeg"])
        ]
    )
    friends = models.ManyToManyField("user.Account", related_name="friends")

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def completion_percentage(self):
        return completion([self.name, self.email, self.about])
    
    @property
    def has_name(self):
        return False if not bool(self.name) else True
    
    @property
    def has_email(self):
        return False if not bool(self.email) else True
    
    @property
    def has_about(self):
        return False if not bool(self.about) else True


class FriendRequest(models.Model):

    receiver = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="receiver")
    sender   = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="sender")
    status   = models.BooleanField(default=False)

    def accept(self):
        if self.status:
            self.receiver.profile.friends.add(self.sender)
            self.sender.profile.friends.add(self.receiver)


class Scheme(models.Model):
    user = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    @property
    def logs(self):
        return LogEntry.objects.filter(user_id=self.user.id)
    @property
    def circles(self):
        return {
            'as_founder':Circle.objects.filter(founder=self.user).order_by('-created'),
            'as_member':Circle.objects.filter(members=self.user).order_by('-created'),
            'all': Circle.objects.filter(Q(founder=self.user) or Q(members=self.user)).order_by('-created')
        }