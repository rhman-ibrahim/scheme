from django.urls import path
from . import views

app_name    = "ping"
urlpatterns = [
    # Update
    path('<str:serial>/udate/status/', views.update_room_status, name="update_room_status"),
]