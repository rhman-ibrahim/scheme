from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # Create
    path('create/', views.create_circle, name="create_circle"),
    path('request/', views.create_request, name="create_request"),
    # Render
    path('', views.retrieve_team_index, name="retrieve_team_index"),
    path('settings/', views.retrieve_team_settings, name="retrieve_team_settings"),
    # Update
    path('import/friends/', views.import_friends, name="import_friends"),
    path('remove/<int:user_id>/', views.remove_circle_member, name="remove_circle_member"),
    path('accept/<int:user_id>/', views.accept_request, name="accept_request"),
    path('reject/<int:user_id>/', views.reject_request, name="reject_request"),
    path('transfer/', views.transfer_circle, name="transfer_circle"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('leave/', views.leave, name="leave"),
    # Delete
    path('delete/<int:id>/', views.delete_request, name="delete_request"),
]