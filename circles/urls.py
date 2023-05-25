from django.urls import path
from . import views


app_name    = "circles"
urlpatterns = [
    path('create/', views.create, name="create"),
    path('invite/', views.invite, name="invite"),
    path('manage/', views.manage, name="manage"),
    path('<str:uuid>/', views.invitation, name="invitation"),
    path('terminate/', views.terminate, name="terminate"),
]