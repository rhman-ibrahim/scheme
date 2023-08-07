from django.urls import path
from . import views


app_name    = "blog"
urlpatterns = [
    # Create
    path('create/', views.create_signal, name="create_signal"),
    # Retrieve
    path('<str:serial>/', views.retrieve_signal, name="retrieve_signal"),
    # Update
    path('<str:serial>/status/update/', views.update_signal_status, name="update_signal_status"),
]