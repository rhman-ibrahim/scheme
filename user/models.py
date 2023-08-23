# Standard libraries
import datetime, pytz

# Django
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import FileExtensionValidator, RegexValidator
from django.contrib.admin.models import LogEntry
from django.utils.crypto import get_random_string
from django.urls import reverse

# Helpers
from helpers.functions import (
    profile_picture_path_handler
)

class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        if not username or not password:
            raise ValueError('a username and a password are required.')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_guest(self, username, password=None):
        if not username or not password:
            raise ValueError('a username and a password are required.')
        user = self.model(username=username, is_guest=True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user              = self.create_user(username=username, password=password)
        user.is_admin     = True
        user.is_staff     = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):

    username       = models.CharField(
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9]{4,16}$', message='this is not a valid username')
        ],
        unique      = True,
        max_length  = 16
    )
    is_active      = models.BooleanField(default=True)
    is_superuser   = models.BooleanField(default=False)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_guest       = models.BooleanField(default=False)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    objects        = UserManager()

    def __str__(self):
        return self.username
    
    @property
    def state(self):
        return "active" if self.is_active == True else "deactive"

    @property
    def actions(self):
        return LogEntry.objects.filter(user_id=self.id).count()
    
    @property
    def is_expired(self):
        if self.is_guest:
            ct = datetime.datetime.now(tz=pytz.timezone('Africa/Cairo'))
            tt = self.created + datetime.timedelta(hours=8)
            df = tt - ct
            return True if df.total_seconds() < 0 else False
        return False

    @property
    def timer(self):
        if self.is_guest:
            tt = self.created + datetime.timedelta(hours=8)
            return tt.strftime("%b %d, %Y %H:%M:%S")
        return None


class Token(models.Model):

    user    = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    key     = models.CharField(max_length=32, default=get_random_string(length=32), null=False, blank=False)
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
    friends = models.ManyToManyField(
        "user.Account",
        related_name="friends",
        related_query_name="friends"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def has_name(self):
        return False if not bool(self.name) else True
    
    @property
    def has_email(self):
        return False if not bool(self.email) else True
    
    @property
    def has_about(self):
        return False if not bool(self.about) else True
    
    def index(self):
        return reverse("mate:retrieve_mate_index", args=[str(self.user.username)])
    
    @property
    def logs(self):
        return LogEntry.objects.filter(user_id=self.user.id)
    
    @property
    def requests(self):

        from team.models import SpaceRequest
        from mate.models import FriendRequest

        query = FriendRequest.objects.filter(
            (Q(receiver=self.user) | Q(receiver=self.user)) & Q(status=2)
        ).distinct().order_by('-id')
        return {
            'firend': {
                'received': query.filter(receiver=self.user),
                'sent': query.filter(sender=self.user),
            },
            'circle': {
                SpaceRequest.objects.filter(user=self.user, status=2).distinct().order_by('-id')
            }
        }
    
    @property
    def circles(self):
        
        from team.models import Space

        query = Space.objects.filter(Q(founder=self.user) | Q(members=self.user)).distinct().order_by('-id')
        return {
            'all': query,
            'as_founder': query.filter(founder=self.user),
            'as_member': query.filter(members=self.user),
        }