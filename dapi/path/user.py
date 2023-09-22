from django.urls import path
from dapi.views.user import AccountViewSet


urlpatterns = [
    path(
        'sign/up/',
        AccountViewSet.as_view({'post':'signup'})
    ),
    path(
        'sign/in/',
        AccountViewSet.as_view({'post':'signin'})
    ),
    path(
        'sign/out/',
        AccountViewSet.as_view({'post':'signout'})
    ),
    path(
        'sign/temporary/',
        AccountViewSet.as_view({'post':'temporary'})
    )
]