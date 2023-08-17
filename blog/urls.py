from django.urls import path
from . import views


app_name    = "blog"
urlpatterns = [
    # Create
    path('create/post/', views.create_post, name="create_post"),
    path('create/comment/', views.create_comment, name="create_comment"),
    # Retrieve
    path('post/<str:serial>/', views.retrieve_post, name="retrieve_post"),
    path('comment/<str:serial>/', views.retrieve_comment, name="retrieve_comment"),
    # Update
    path('<str:serial>/status/update/', views.update_signal_status, name="update_signal_status"),
]