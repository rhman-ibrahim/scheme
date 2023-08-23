from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    # Create
    path('create/request/', views.create_friend_request, name='create_friend_request'),
    # Retrieve
    path('<str:username>/', views.retrieve_mate_index, name='retrieve_mate_index'),
    # Update
    path('accept/request/<int:req>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/request/<int:req>/', views.reject_friend_request, name='reject_friend_request'),
    # Delete
    path('delete/request/<int:req>/', views.delete_friend_request, name='delete_friend_request')
]