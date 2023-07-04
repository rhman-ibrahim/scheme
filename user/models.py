import qrcode
# Django
from django.db.models import Q
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.contrib.admin.models import LogEntry
from django.db import models
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
        unique     = True,
        max_length = 16
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
        return f"{self.username}'s account"
    
    @property
    def state(self):
        return "active" if self.is_active == True else "deactive"

    @property
    def actions(self):
        return LogEntry.objects.filter(user_id=self.id).count()

class Token(models.Model):

    user    = models.OneToOneField("user.Account", on_delete=models.CASCADE, primary_key=True)
    value   = models.CharField(max_length=32, default=get_random_string(length=32), null=False, blank=False)
    ready   = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def path(self):
        return f'/media/user/tokens/{self.user.username}.png'

    def save(self, *args, **kwargs):
        qr = qrcode.make(self.value)
        qr.save(f'{MEDIA_ROOT}/user/tokens/{self.user.username}.png')
        super(Token, self).save(*args, **kwargs)