from django.urls import path
from .views.ping import RoomViewSet
from .views.user import AccountViewSet, TokenViewSet
from .views.ping import MessageViewSet, StatusViewSet
from .views.team import SpaceViewSet


app_name    = "api"
urlpatterns = [
    # CSRF
    path(
        'csrf/',
        TokenViewSet.as_view({'get':'csrf'})
    ),
    # Account
    path(
        'user/sign/up/',
        AccountViewSet.as_view({'post':'signup'})
    ),
    path(
        'user/sign/in/',
        AccountViewSet.as_view({'post':'signin'})
    ),
    # Room & Message
    path(
        'room/<str:identifier>/messages/',
        RoomViewSet.as_view({'get':'messages'})
    ),
    path(
        'flash/',
        MessageViewSet.as_view({'get':'flash'})
    ),
    # Space
    path(
        'create/circle/',
        SpaceViewSet.as_view({'post':'create'})
    ),
    path(
        'circle/<int:pk>/info/',
        SpaceViewSet.as_view({'get':'info'})
    )
]