from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status


def resource(view):
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {'message':'the requested resource does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
    return wrapper
