from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # All
    path('create/', views.create, name="create"),
    path('request/<str:serial>/', views.create_request, name="request"),
    # Founder
    path('put/', views.add_founder_friends, name="add_founder_friends"),
    path('approve/<int:user_id>/', views.approve, name="approve"),
    path('reject/<int:user_id>/', views.reject, name="reject"),
    path('remove/<int:user_id>/', views.remove, name="remove"),
    path('transfer/', views.transfer, name="transfer"),
    # Memebers
    path('login/', views.login, name="login"),
    path('browse/', views.browse, name="browse"),
    path('logout/', views.logout, name="logout"),
    path('leave/', views.leave, name="leave"),
]