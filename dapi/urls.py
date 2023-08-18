from django.urls import path
from .views import RoomViewSet, CircleViewSet

app_name    = "api"
urlpatterns = [
    # Retrieve
    path('create/circle/', CircleViewSet.as_view({'post':'create'})),
    path('circle/<int:pk>/info/', CircleViewSet.as_view({'get':'info'})),
    path('room/<str:serial>/messages/', RoomViewSet.as_view({'get':'messages'})),
]