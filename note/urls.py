from django.urls import path
from note import views


app_name    = "note"
urlpatterns = [
    # Verify
    path('signin/', views.token_signin, name='token_signin'),
    path('login/', views.secret_verify, name="secret_verify"),
    # Update
    path('update/token/', views.update_token, name='update_token'),
    path('reset/account/password/', views.reset_account_password, name='reset_account_password'),
    # PDF
    path('pdf/', views.pdf, name='pdf'),
]