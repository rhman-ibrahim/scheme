from django.contrib import admin
from user.models import Account, Token, Profile


# Register your models here.

admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(Token)