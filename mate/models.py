# Django
from django.db.models import Q
from django.contrib.admin.models import LogEntry
from django.core.validators import FileExtensionValidator
from django.contrib.admin.models import LogEntry
from django.db import models
# Helpers
from helpers.functions import completion
# Circles
from circles.models import Circle


def profile_picture_path_handler(instance, filename):
    # renames the updated profile picture with the user's username.
    return f'user/profile/pictures/{instance.account.username}.{filename.split(".")[-1]}'

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

    user = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)

    @property
    def logs(self):
        return LogEntry.objects.filter(user_id=self.user.id)
    
    @property
    def circles(self):
        return {
            'as_founder':Circle.objects.filter(founder=self.user),
            'as_member':Circle.objects.filter(Q(members=self.user))
        }
