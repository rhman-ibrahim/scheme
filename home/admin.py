from django.contrib import admin
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)