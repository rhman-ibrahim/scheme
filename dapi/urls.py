from django.urls import path
from .views.ping import RoomViewSet
from .views.user import AccountViewSet
from .views.ping import MessageViewSet, StatusViewSet
from .views.team import SpaceViewSet


app_name    = "api"
urlpatterns = [
    # Account
    path('csrf/', AccountViewSet.as_view({'get':'csrf'})),
    path('signup/', AccountViewSet.as_view({'post':'signup'})),
    path('signin/', AccountViewSet.as_view({'post':'signin'})),
    # Room & Message
    path('room/<str:identifier>/messages/', RoomViewSet.as_view({'get':'messages'})),
    path('flash/', MessageViewSet.as_view({'get':'flash'})),
    # Space
    path('create/circle/', SpaceViewSet.as_view({'post':'create'})),
    path('circle/<int:pk>/info/', SpaceViewSet.as_view({'get':'info'})),
    # Status
    path('connection/status/', StatusViewSet.as_view({'get':'status'})),
    path('connection/check/', StatusViewSet.as_view({'get':'check'})),
]