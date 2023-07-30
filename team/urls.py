from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # All
    path('delete/<int:id>/', views.delete_circle_request, name="delete_circle_request"),
    path('request/', views.create_circle_request, name="create_circle_request"),
    path('create/', views.create, name="create"),
    # Founder
    path('approve/<int:user_id>/', views.approve, name="approve"),
    path('reject/<int:user_id>/', views.reject, name="reject"),
    path('remove/<int:user_id>/', views.remove, name="remove"),
    path('transfer/', views.transfer, name="transfer"),
    path('put/', views.put, name="put"),
    # Memebers
    path('browse/', views.browse, name="browse"),
    path('logout/', views.logout, name="logout"),
    path('leave/', views.leave, name="leave"),
    path('login/', views.login, name="login"),
]