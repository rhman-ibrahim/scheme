from django.urls import path
from user import views


app_name    = "user"
urlpatterns = [
    path('', views.pdf, name="pdf"),
    path('settings/', views.account, name="account"),
    path('<str:username>/', views.friend, name="friend"),
    path('update/token/', views.update_token, name='update_token'),
    path('update/password/', views.update_password, name='update_password'),
    path('update/profile/', views.update_profile, name='update_profile'),
    path('deactivate/', views.deactivate, name="deactivate"),
    path('sign/out/', views.sign_out, name='sign_out'),
]