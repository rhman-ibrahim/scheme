# Standard libraries
import datetime, pytz

# Django
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.admin.models import LogEntry
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from helpers.functions import generate_identifier


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
    key     = models.CharField(max_length=32, default=generate_identifier, null=False, blank=False)
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
    friends = models.ManyToManyField("self", symmetrical=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def index(self):
        return reverse("mate:retrieve_friend_index", args=[str(self.user.username)])

    @property
    def has_name(self):
        return False if not bool(self.name) else True
    
    @property
    def has_email(self):
        return False if not bool(self.email) else True
    
    @property
    def has_about(self):
        return False if not bool(self.about) else True
    
    @property
    def logs(self):
        return LogEntry.objects.filter(user_id=self.user.id)
    
    @property
    def requests(self):
        from mate.models import FriendRequest, SpaceRequest
        return {
            'friend': {
                'received': FriendRequest.objects.filter(receiver=self.user, status=2).distinct().order_by('-id'),
                'sent': FriendRequest.objects.filter(sender=self.user, status=2).distinct().order_by('-id'),
            },
            'space': SpaceRequest.objects.filter(user=self.user, status=2).distinct().order_by('-id')
        }
    
    @property
    def spaces(self):
        from team.models import Space
        query = Space.objects.filter(Q(founder=self.user) | Q(members=self.user)).distinct().order_by('-id')
        return {
            'all': query,
            'as_founder': query.filter(founder=self.user),
            'as_member': query.filter(members=self.user),
        }