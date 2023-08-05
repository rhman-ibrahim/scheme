from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Nav
    path('terminate/', views.terminate, name="terminate"),
    path('settings/', views.settings, name="settings"),
    path('guest/', views.guest, name="guest"),
    path('', views.nav, name='nav'),
    # Sign
    path('signin/guest/', views.signin_guest, name='signin_guest'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    # Token
    path('update/token/', views.update_token, name='update_token'),
    path('verify/', views.verify, name='verify'),
    path('token/', views.token, name='token'),
    # Update
    path('update/password/', views.update_password, name='password'),
    path('delete/', views.delete_account, name='delete_account'),
    path('reset/', views.reset, name='reset'),
]