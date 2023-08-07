from django.urls import path
from . import views

app_name    = "dapi"
urlpatterns = [
    # Retrieve
    path('<str:serial>/', views.retrieve_room_messages, name="retrieve_room_messages")
]