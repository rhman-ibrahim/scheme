from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # All
    path('create/', views.create, name="create"),
    path('link/<str:serial>/', views.link, name="link"),
    # Founder
    path('refresh/', views.refresh, name="refresh"),
    path('reject/<int:user_id>/', views.reject, name="reject"),
    path('remove/<int:user_id>/', views.remove, name="remove"),
    path('approve/<int:user_id>/', views.approve, name="approve"),
    # Members
    path('leave/', views.leave, name="leave"),
    path('login/<str:serial>/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('browse/', views.browse, name="browse"),
]