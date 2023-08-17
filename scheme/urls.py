from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dapi.urls'), name="api"),
    path('user/', include('user.urls'), name="user"),
    path('mate/', include('mate.urls'), name="mate"),
    path('team/', include('team.urls'), name="team"),
    # path('blog/', include('blog.urls'), name="blog"),
    path('ping/', include('ping.urls'), name="ping"),
    path('home/', include('home.urls'), name="home"),

]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
