from django.urls import path
from . import views


app_name    = "mates"
urlpatterns = [
    # Update
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('update/info/', views.update_profile_info, name='info'),
]