from django.urls import path
from .views import RoomViewSet, SpaceViewSet, MessageViewSet

app_name    = "api"
urlpatterns = [
    # Retrieve
    path('create/circle/', SpaceViewSet.as_view({'post':'create'})),
    path('circle/<int:pk>/info/', SpaceViewSet.as_view({'get':'info'})),
    path('room/<str:serial>/messages/', RoomViewSet.as_view({'get':'messages'})),
    path('flash/', MessageViewSet.as_view({'get':'flash'}))
]