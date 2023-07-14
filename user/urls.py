from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Nav
    path('back/', views.back, name='back'),
    path('settings/', views.settings, name="settings"),
    path("navigate/", views.navigate, name="navigate"),
    # Sign
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    # Token
    path('update/token/', views.update_token, name='update_token'),
    path('verify/', views.verify, name='verify'),
    path('token/', views.token, name='token'),
    # Update
    path('update/password/', views.update_password, name='password'),
    path('reset/', views.reset, name='reset'),
]