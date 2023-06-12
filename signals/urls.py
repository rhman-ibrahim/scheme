from django.urls import path
from . import views


app_name    = "signals"
urlpatterns = [
    path('', views.index, name="hypotheses"),
    path('create/opportunity/', views.create_opportunity, name="create_opportunity"),
    path('create/problem/', views.create_problem, name="create_problem"),
]