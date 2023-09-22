from django.urls import path, include

app_name    = "dapi"
urlpatterns = [
    path('home/', include('dapi.path.home')),
    path('room/', include('dapi.path.room')),
    path('space/', include('dapi.path.space')),
    path('user/', include('dapi.path.user')),
    path('jwt/', include('dapi.path.jwt')),
]