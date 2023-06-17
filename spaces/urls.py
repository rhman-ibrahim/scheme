from django.urls import path
from . import views
from . import api

app_name    = "spaces"
urlpatterns = [
    path('', views.index, name="home"),
    path('<str:serial>/', api.room_messages)
]