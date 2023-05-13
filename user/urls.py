from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    # Templates
    ## Anonymous
    path('auth/', views.index, name="index"),
    path('identified/', views.identified, name="identified"),
    ## Authenticated
    path('settings/', views.settings, name="settings"),
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
    path('update/info/', views.update_profile_info, name='info'),
    # Functionalities
    path("navigate/", views.navigate, name="navigate"),
    ## Anonynous
    path('lazy/signup/', views.lazy_signup, name="lazy"),
    ## Authenticated
    path('token/', views.token, name='token'),
    path('verification/cancel/', views.cancel, name='cancel'),
    path('signout/', views.signout, name='signout'),
]