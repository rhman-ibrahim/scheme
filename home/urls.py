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
    path("sign/", views.sign, name="sign"),
]