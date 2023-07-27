from django.urls import path
from . import views


app_name    = "blog"
urlpatterns = [
    path('create/', views.create_signal, name="create_signal"),
    path('status/toggle/<str:serial>/', views.update_signal_status, name="update_signal_status"),
    path('<str:serial>/', views.get_signal, name="get_signal"),
]