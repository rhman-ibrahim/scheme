from django.urls import path
from note import views


app_name    = "note"
urlpatterns = [
    path('reset/', views.reset, name='reset'),
    path('signin/', views.signin, name='signin'),
    path('update/token/', views.update_token, name='update_token'),
    path('login/', views.login, name="login"),
    path('pdf/', views.pdf, name='pdf'),
]