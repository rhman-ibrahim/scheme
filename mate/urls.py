from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    # Create
    path('create/request/', views.create_request, name='create_request'),
    # Retrieve
    path('<str:username>/', views.retrieve_mate_index, name='retrieve_mate_index'),
    # Update
    path('update/info/', views.update_profile_info, name='info'),
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('accept/request/<int:req>/', views.accept_request, name='accept_request'),
    path('reject/request/<int:req>/', views.reject_request, name='reject_request'),
    # Delete
    path('delete/request/<int:req>/', views.delete_request, name='delete_request')
]