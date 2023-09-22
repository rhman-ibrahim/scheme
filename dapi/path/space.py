from django.urls import path
from dapi.views.team import SpaceViewSet


urlpatterns = [
    path(
        'create/circle/',
        SpaceViewSet.as_view({'post':'create'})
    ),
    path(
        'circle/<int:pk>/info/',
        SpaceViewSet.as_view({'get':'info'})
    )
]