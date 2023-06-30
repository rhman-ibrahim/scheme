from django.urls import path
from . import views


app_name    = "circle"
urlpatterns = [
    path('create/', views.create, name="create"),
    path('link/<str:serial>/', views.link, name="link"),
    path('approve/<int:user_id>/', views.approve, name="approve"),
    path('reject/<int:user_id>/', views.reject, name="reject"),
    path('remove/<int:user_id>/', views.remove, name="remove"),
    path('open/<str:serial>/', views.open, name="open"),
    path('browse/', views.browse, name="browse"),
    path('close/', views.close, name="close"),
    path('leave/', views.leave, name="leave"),
]