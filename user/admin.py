from django.contrib import admin
from user.models import Account, Token, Profile


admin.site.register(Account)
admin.site.register(Token)
admin.site.register(Profile)