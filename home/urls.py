from django.urls import path
from . import views


app_name    = "home"
urlpatterns = [
    # Render
    path('', views.render_home_index, name="render_home_index")
]