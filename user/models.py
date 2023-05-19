import qrcode

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.crypto import get_random_string
from django.contrib.admin.models import LogEntry
from django.db import models

from scheme.settings import MEDIA_ROOT
from helpers.functions import completion




def profile_picture_path_handler(instance, filename):
    # renames the updated profile picture with the user's username.
    return f'user/profile/pictures/{instance.account.username}.{filename.split(".")[-1]}'


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username or not password: raise ValueError('a username and a password are required.')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_lazy_user(self, username, password=None):
        if not username or not password: raise ValueError('a username and a password are required.')
        user = self.model(username=username, is_lazy=True)
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
    is_lazy        = models.BooleanField(default=False)
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
        return f'/media/user/account/tokens/{self.user.username}.png'

    def save(self, *args, **kwargs):
        qr = qrcode.make(self.value)
        qr.save(f'{MEDIA_ROOT}/user/account/tokens/{self.user.username}.png')
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

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def completion_percentage(self):
        return completion([self.name, self.email, self.about])