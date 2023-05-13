from django.contrib import admin
from .models import followRequest, Connection, joinRequest, Circle


admin.site.register(followRequest)
admin.site.register(Connection)
admin.site.register(joinRequest)
admin.site.register(Circle)
