from django.urls import path
from . import views


app_name    = "home"
urlpatterns = [
    # Render
    path('', views.index, name="index"),
    path('reset/', views.reset, name="reset"),
    path('space/', views.space, name="space"),
    path('account/', views.account, name="account"),
    path('404/', views.object_not_found, name="404"),
    path('sign/up/', views.sign_up, name="sign_up"),
    path('sign/in/', views.sign_in, name="sign_in"),
    path("sign/", views.sign, name="sign"),
]