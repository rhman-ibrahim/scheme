from django.urls import path
from . import views


app_name    = "circle"
urlpatterns = [
    path('create/', views.create, name="create"),
    #
    path('join/<str:serial>/', views.join, name="join"),
    path('open/<str:serial>/', views.open, name="open"),
    path('page/<str:serial>/', views.page, name="page"),
    path('exit/<str:serial>/', views.close, name="exit"),
    #
    path('approve/<str:serial>/<int:user_id>/', views.approve, name="approve"),
    path('reject/<str:serial>/<int:user_id>/', views.reject, name="reject"),
    path('remove/<str:serial>/<int:user_id>/', views.remove, name="remove")
]