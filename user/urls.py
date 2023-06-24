from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Process
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verify/', views.verify, name='verify'),
    path('reset/', views.reset, name='reset'),
    # Update
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('update/password/', views.update_password, name='password'),
    path('update/token/', views.update_token, name='update_token'),
    path('update/info/', views.update_profile_info, name='info'),
    # Template
    path('token/', views.token, name='token'),
    path('settings/', views.settings, name="settings"),
    path("navigate/", views.navigate, name="navigate"),
    path('signout/', views.signout, name='signout'),
    path('back/', views.back, name='back'),
]