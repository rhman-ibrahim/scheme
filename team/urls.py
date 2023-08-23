from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # Create
    path('create/', views.create_circle, name="create_circle"),
    
    # Render
    path('', views.retrieve_team_index, name="retrieve_team_index"),
    # Update
    path('import/friends/', views.import_friends, name="import_friends"),
    path('remove/<int:user_id>/', views.remove_circle_member, name="remove_circle_member"),
    path('transfer/', views.transfer_circle, name="transfer_circle"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('leave/', views.leave, name="leave"),
]