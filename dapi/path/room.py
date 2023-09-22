from django.urls import path
from dapi.views.ping import RoomViewSet


urlpatterns = [
    path(
        'room/<str:identifier>/messages/',
        RoomViewSet.as_view({'get':'messages'})
    )
]