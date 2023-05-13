from django.urls import path
from . import views


app_name    = "signals"
urlpatterns = [

    # Index (Home)
    path('', views.read_ideas, name="read_ideas"),

    # Signal
    path('signal/', views.create_signal, name="create_signal"),
    path('signal/update/<str:id>/', views.update_signal, name="update_signal"),
    path('signal/delete/<str:id>/', views.delete_signal, name="delete_signal"),

    # Idea
    path('idea/<str:id>/', views.read_idea, name="read_idea"),

    # Concern
    path('concern/<str:id>/', views.read_concern, name="read_concern"),

    # Test
    path('test/<str:id>/', views.read_test, name="read_test"),

    # Result
    path('result/<str:id>/', views.read_result, name="read_result"),

    # Note
    path('note/', views.create_note, name="create_note"),
    
    # Comment
    path('comment/', views.create_comment, name="create_comment"),
    path('comment/update/<str:id>/', views.update_comment, name="update_comment"),
    path('comment/delete/<str:id>/', views.delete_comment, name="delete_comment"),
    
]