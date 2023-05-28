from django.urls import path
from . import views


app_name    = "circles"
urlpatterns = [
    path('create/', views.create, name="create"),
    path('manage/', views.manage, name="manage"),
    path('ask/<str:uuid>/', views.ask, name="ask"),
    path('open/<str:uuid>/', views.open, name="open"),
    path('approve/<int:cid>/<int:uid>/', views.approve, name="approve"),
    path('reject/<int:cid>/<int:uid>/', views.reject, name="reject"),
    path('close/', views.close, name="close"),
]