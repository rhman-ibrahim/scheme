from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    # Create
    path('create/friend/request/', views.create_friend_request, name='create_friend_request'),
    path('create/circle/request/', views.create_circle_request, name="create_circle_request"),
    # Retrieve
    path('<str:username>/', views.retrieve_mate_index, name='retrieve_mate_index'),
    # Update
    path('accept/friend/<int:req>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/friend/<int:req>/', views.reject_friend_request, name='reject_friend_request'),
    path('accept/member/<int:user_id>/', views.accept_circle_request, name="accept_circle_request"),
    path('reject/member/<int:user_id>/', views.reject_circle_request, name="reject_circle_request"),
    # Delete
    path('cancel/friend/<int:req>/', views.delete_friend_request, name='delete_friend_request'),
    path('cancel/member/<int:id>/', views.delete_circle_request, name="delete_circle_request")
]