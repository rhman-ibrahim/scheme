from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Create
    path('signup/', views.create_account, name='create_account'),
    path('signin/guest/', views.create_guest, name='create_guest'),
    # Retrieve
    path('settings/', views.retrieve_account, name="retrieve_account"),
    path('token/', views.retrieve_token, name='retrieve_token'),
    # Update
    path('update/password/', views.update_account_password, name='update_account_password'),
    path('deactivate/', views.update_account_status, name="update_account_status"),
    path('reset/', views.reset_account_password, name='reset_account_password'),
    path('update/token/', views.update_token, name='update_token'),
    path('signout/', views.signout, name='signout'),
    # Validate
    path('signin/', views.signin, name='signin'),
    path('verify/', views.verify, name='verify'),
    # Delete
    path('delete/', views.delete_account, name='delete_account'),
]