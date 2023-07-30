# URLS
from django.urls import reverse

# Validators
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# DB
from django.db.models import Q
from django.db import models

# Models
from django.contrib.admin.models import LogEntry
from team.models import Circle, CircleRequest

# Helpers
from helpers.functions import (
    completion, profile_picture_path_handler, generate_serial
)


REQUEST_STATUS = (
    (0, "Rejected"),
    (1, "Accepted"),
    (2, "Pending"),
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
    

class FriendRequest(models.Model):

    status   = models.IntegerField(choices=REQUEST_STATUS, default=2, blank=False, null=False)
    serial   = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    receiver = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="receiver")
    sender   = models.ForeignKey("user.Account", on_delete=models.CASCADE, related_name="sender")
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def accept(self):
        return reverse("mate:accept_friend_request", args=[str(self.id)])

    def reject(self):
        return reverse("mate:reject_friend_request", args=[str(self.id)])

    def cancel(self):
        return reverse("mate:delete_friend_request", args=[str(self.id)])
    
    def validate_unique(self, exclude=None):
        # Check if there is an existing friend request with the sender and receiver fields swapped
        if FriendRequest.objects.filter(sender=self.receiver, receiver=self.sender).exists():
            raise ValidationError('A friend request already exists between these users.')
        # Call the parent validate_unique method to check for any other unique constraints
        super(FriendRequest, self).validate_unique(exclude=exclude)
    
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FriendRequest, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('sender', 'receiver')
        

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
    def circle_requests(self):
        return CircleRequest.objects.filter(user=self.user, status=2).order_by('-id')
    
    @property
    def circles(self):
        return {
            'all': Circle.objects.filter(Q(founder=self.user) | Q(members=self.user)).order_by('-created'),
            'as_founder':Circle.objects.filter(founder=self.user).order_by('-created'),
            'as_member':Circle.objects.filter(members=self.user).order_by('-created')
        }