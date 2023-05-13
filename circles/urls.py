from django.urls import path
from . import views


app_name    = "circles"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('manage/<str:serial>/', views.manage, name="manage"),
    path('connect/', views.connect, name="connect"),
    path('create/connection/<str:username>/', views.create_connection, name="create_connection"),
    path('accept/connection/<int:id>/', views.accept_connection, name="accept_connection"),
    path('reject/connection/<int:id>/', views.reject_connection, name="reject_connection"),
]