from django.urls import path
from . import views


app_name    = "team"
urlpatterns = [
    # Create
    path('create/', views.create_space, name="create_space"),
    
    # Render
    path('', views.retrieve_team_index, name="retrieve_team_index"),
    # Update
    path('import/friends/', views.import_friends, name="import_friends"),
    path('remove/<int:user_id>/', views.remove_space_member, name="remove_space_member"),
    path('transfer/', views.transfer_space, name="transfer_space"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('leave/', views.leave, name="leave"),
]