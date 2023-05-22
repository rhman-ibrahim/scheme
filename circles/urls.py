from django.urls import path
from . import views


app_name    = "circles"
urlpatterns = [
    path('connect/', views.index, name="connect"),
    path('<str:uuid>/', views.invitation, name="invitation"),
]