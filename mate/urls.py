from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    # Update
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('update/info/', views.update_profile_info, name='info'),
    # Friends
    path('create/friend/request/', views.create_friend_request, name='create_friend_request'),
    path('delete/friend/request/<int:request_id>/', views.delete_friend_request, name='delete_friend_request'),
    path('accept/friend/request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/friend/request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]