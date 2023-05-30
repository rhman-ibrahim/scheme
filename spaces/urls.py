from django.urls import path
from . import views


app_name    = "spaces"
urlpatterns = [
    path('', views.index, name="home")
]