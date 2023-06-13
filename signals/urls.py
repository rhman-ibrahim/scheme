from django.urls import path
from . import views


app_name    = "signals"
urlpatterns = [
    path('', views.list, name="list"),
    path('create/opportunity/', views.create_opportunity, name="create_opportunity"),
    path('create/problem/', views.create_problem, name="create_problem"),
    path('create/hypothesis/', views.create_hypothesis, name="create_hypothesis"),
    path('<str:uuid>/', views.detail, name="signal")
]