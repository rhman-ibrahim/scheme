from django.urls import path
from . import views


app_name    = "mate"
urlpatterns = [
    path('create/request/', views.create_friend_request, name='create_friend_request'),
    path('accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/<int:id>/', views.reject_friend_request, name='reject_friend_request'),
    path('cancel/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    path('create/space/request/', views.create_space_request, name="create_space_request"),
    path('accept/request/<int:id>/', views.accept_space_request, name="accept_space_request"),
    path('reject/request/<int:id>/', views.reject_space_request, name="reject_space_request"),
    path('cancel/request/<int:id>/', views.delete_space_request, name="delete_space_request"),
    path('create/space/invitation/', views.create_space_invitation, name="create_space_invitation"),
    path('accept/invitation/<int:id>/', views.accept_space_invitation, name="accept_space_invitation"),
    path('reject/invitation/<int:id>/', views.reject_space_invitation, name="reject_space_invitation"),
    path('cancel/invitation/<int:id>/', views.delete_space_invitation, name="delete_space_invitation"),
]