from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Templates
    path('auth/', views.index, name="index"),
    path('identified/', views.identified, name="identified"),
    path('settings/', views.settings, name="settings"),
    path('token/', views.token, name='token'),
    # Forms
    ## Anonymous
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verify/', views.verify, name='verify'),
    ## Identified
    path('reset/', views.reset, name='reset'),
    ## Authenticated
    path('update/picture/', views.update_profile_picture, name='picture'),
    path('update/password/', views.update_password, name='password'),
    path('update/token/', views.update_token, name='update_token'),
    path('update/info/', views.update_profile_info, name='info'),
    # Functionalities
    path('reset/cancel/', views.cancel, name='cancel'),
    path("navigate/", views.navigate, name="navigate"),
    path('signout/', views.signout, name='signout'),
    path('guest/', views.guest_login, name="guest"),
]