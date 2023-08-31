from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name="home"),
    path('user/', include('user.urls'), name="user"),
    path('note/', include('note.urls'), name="note"),
    path('mate/', include('mate.urls'), name="mate"),
    path('team/', include('team.urls'), name="team"),
    path('ping/', include('ping.urls'), name="ping"),
    path('api/', include('dapi.urls'), name="api"),
]