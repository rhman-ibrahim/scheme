# URLS
from django.urls import reverse

# Validators
from django.core.validators import FileExtensionValidator

# DB
from django.db.models import Q
from django.db import models

# Models
from django.contrib.admin.models import LogEntry
from mate.models.friends import FriendRequest
from team.models import Circle

# Helpers
from helpers.functions import (
    completion, profile_picture_path_handler
)


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

    def index(self):
        return reverse("mate:profile", args=[str(self.user.username)])

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
    


class Scheme(models.Model):

    user    = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    friends = models.ManyToManyField("user.Account", related_name="friends", related_query_name="friends")

    def __str__(self):
        return self.user.username

    @property
    def logs(self):
        return LogEntry.objects.filter(user_id=self.user.id)
    
    @property
    def friend_requests(self):
        return {
            'received': FriendRequest.objects.filter(receiver=self.user, status=2).order_by('-id'),
            'sent': FriendRequest.objects.filter(sender=self.user, status=2).order_by('-id')
        }
    
    @property
    def circles(self):
        return {
            'all': Circle.objects.filter(Q(founder=self.user) or Q(members=self.user)).order_by('-created'),
            'as_founder':Circle.objects.filter(founder=self.user).order_by('-created'),
            'as_member':Circle.objects.filter(members=self.user).order_by('-created')
        }