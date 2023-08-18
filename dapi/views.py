# REST
from rest_framework import status, viewsets
from rest_framework.response import Response

# Django
from django.core.exceptions import ObjectDoesNotExist

# Models
from team.models import Circle
from ping.models import Message

# Serializers
from .serializers import (
    MessageSerializer, CircleSerializer, CirclePostSerializer
)

# Helpers
from helpers.functions import (
    secret,
)

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


class CircleViewSet(viewsets.ViewSet):

    @resource
    def info(self, request, pk=None):
        return Response(
            CircleSerializer(Circle.objects.get(id=pk)).data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = CirclePostSerializer(
            data = {
                "password": secret(request.POST.get('password')) if bool(request.POST.get('password')) else None,
                "name": request.POST.get('name'),
                "founder": request.user.id,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RoomViewSet(viewsets.ViewSet):
    
    @resource
    def messages(self, request, serial=None):
        return Response(
            MessageSerializer(
                [{'sender': m.sender.username,'body': m.body} for m in Message.objects.filter(room__serial=serial)[:100]],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )