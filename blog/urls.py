from django.urls import path
from . import views


app_name    = "blog"
urlpatterns = [

    path('create/', views.create_signal, name="create_signal"),
    
    path('status/toggle/<str:serial>/', views.update_status, name="update_status"),

    path('', views.list, name="list"),
    path('<str:serial>/', views.detail, name="signal"),
    
]