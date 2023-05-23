from django.urls import path
from . import views


app_name    = "circles"
urlpatterns = [
    path('connect/', views.index, name="connect"),
    path('create/', views.create, name="create"),
    path('manage/', views.manage, name="manage"),
    path('<str:uuid>/', views.invitation, name="invitation"),
]