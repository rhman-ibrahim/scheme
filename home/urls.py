from django.urls import path
from . import views


app_name    = "home"
urlpatterns = [
    # Render
    path('', views.retrieve_home_index, name="retrieve_home_index"),
    path('404/', views.resource_not_found, name="resource_not_found"),
    path('cancel/', views.cancel, name="cancel")
]