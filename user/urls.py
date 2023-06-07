from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Forms
    path('reset/', views.reset, name='reset'),
    path('verify/', views.verify, name='verify'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('update/password/', views.update_password, name='password'),
    path('update/token/', views.update_token, name='update_token'),
    path('update/info/', views.update_profile_info, name='info'),
    # Functionalities
    path("navigate/", views.navigate, name="navigate"),
    path('signout/', views.signout, name='signout'),
    # Templates
    path('guest/', views.guest, name="guest"),
    path('identified/', views.identified, name="identified"),
    path('settings/', views.settings, name="settings"),
    path('token/', views.token, name='token')
]