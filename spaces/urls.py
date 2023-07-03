from django.urls import path
from . import views
from . import api

app_name    = "spaces"
urlpatterns = [
    path('<str:serial>/', api.room_messages)
]