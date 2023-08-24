from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls'), name="user"),
    path('mate/', include('mate.urls'), name="mate"),
    path('team/', include('team.urls'), name="team"),
    path('ping/', include('ping.urls'), name="ping"),
    path('home/', include('home.urls'), name="home"),
    path('api/', include('dapi.urls'), name="api"),
]