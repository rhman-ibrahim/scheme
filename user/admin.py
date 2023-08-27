from django.contrib import admin
from user.models import Account, Profile, Token


admin.site.register(Account)
admin.site.register(Token)
admin.site.register(Profile)