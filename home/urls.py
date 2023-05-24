from django.urls import path
from . import views


app_name    = "home"
urlpatterns = [
    path('', views.index, name="index"),
    path('user/', views.user, name="user"),
    path('circles/', views.circles, name="circles"),
    path('spaces/', views.spaces, name="spaces"),
    path('signals/', views.signals, name="signals"),
]