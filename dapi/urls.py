from django.urls import path
from .views import MessageViewSet
from team.api import SpaceViewSet
from ping.api import RoomViewSet
from user.api import AccountViewSet


app_name    = "api"
urlpatterns = [
    # Retrieve
    path('flash/', MessageViewSet.as_view({'get':'flash'})),
    path('signup/', AccountViewSet.as_view({'post':'signup'})),
    path('signin/', AccountViewSet.as_view({'post':'signin'})),
    path('create/circle/', SpaceViewSet.as_view({'post':'create'})),
    path('circle/<int:pk>/info/', SpaceViewSet.as_view({'get':'info'})),
    path('room/<str:serial>/messages/', RoomViewSet.as_view({'get':'messages'}))
]