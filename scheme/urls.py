from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls'), name="home"),
    path('user/', include('user.urls'), name="user"),
    path('signals/', include('signals.urls'), name="signals"),
    path('circles/', include('circles.urls'), name="circles")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
