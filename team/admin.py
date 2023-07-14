from django.contrib import admin
from .models import Circle, CircleRequest, CircleMembership


admin.site.register(Circle)
admin.site.register(CircleRequest)
admin.site.register(CircleMembership)