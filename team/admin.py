from django.contrib import admin
from .models import Circle, CircleRequests, CircleMembership


admin.site.register(Circle)
admin.site.register(CircleRequests)
admin.site.register(CircleMembership)