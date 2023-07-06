from django.urls import path
from . import views

app_name    = "dapi"
urlpatterns = [
    path('<str:serial>/', views.room_messages)
]