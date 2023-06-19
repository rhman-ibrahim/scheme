from django.urls import path
from . import views


app_name    = "signals"
urlpatterns = [

    path('create/opportunity/', views.create_opportunity, name="create_opportunity"),
    path('create/hypothesis/', views.create_hypothesis, name="create_hypothesis"),
    path('create/problem/', views.create_problem, name="create_problem"),
    
    path('status/toggle/<str:serial>/', views.update_status, name="update_status"),

    path('', views.list, name="list"),
    path('<str:serial>/', views.detail, name="signal"),
    
]