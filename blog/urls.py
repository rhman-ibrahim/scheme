from django.urls import path
from . import views


app_name    = "blog"
urlpatterns = [
    # Create
    path('create/', views.create_post, name="create_post"),
    # Retrieve
    path('<str:serial>/', views.retrieve_post, name="retrieve_post"),
    # Update
    path('<str:serial>/status/update/', views.update_signal_status, name="update_signal_status"),
]