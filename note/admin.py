from django.contrib import admin
from .models import Token, Secret


admin.site.register(Token)
admin.site.register(Secret)