from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    # Template
    path('<str:username>/', views.profile, name='profile'),
    # Update
    path('update/info/', views.update_profile_info, name='info'),
    path('update/picture/', views.update_profile_picture, name='picture'),
    # Friend Requests
    path('create/friend/request/', views.create_friend_request, name='create_friend_request'),
    path('accept/friend/request/<int:req>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/friend/request/<int:req>/', views.reject_friend_request, name='reject_friend_request'),
    path('delete/friend/request/<int:req>/', views.delete_friend_request, name='delete_friend_request')
]