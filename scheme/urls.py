from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('circles/', include('circles.urls'), name="circles"),
    path('signals/', include('signals.urls'), name="signals"),
    path('spaces/', include('spaces.urls'), name="spaces"),
    path('tasks/', include('tasks.urls'), name="tasks"),
    path('user/', include('user.urls'), name="user"),
    path('home/', include('home.urls'), name="home"),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
