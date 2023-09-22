from django.urls import path
from dapi.views.ping import MessageViewSet
from dapi.views.home import WidgetViewSet


urlpatterns = [
    path(
        'widgets/<str:view>/',
        WidgetViewSet.as_view({'get':'by_view'})
    ),
    path(
        'widgets/name/<str:name>/',
        WidgetViewSet.as_view({'get':'by_name'})
    ),
    path(
        'widgets/<str:name>/<str:note>/',
        WidgetViewSet.as_view({'get':'by_note'})
    ),
    # Messages
    path(
        'flash/',
        MessageViewSet.as_view({'get':'flash'})
    )
]