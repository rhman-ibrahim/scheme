# Standard libraries
import datetime, pytz

# Django
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.crypto import get_random_string
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import RegexValidator
from django.contrib.admin.models import LogEntry

# Scheme
from scheme.settings import MEDIA_ROOT


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
        super(Token, self).save(*args, **kwargs)