# REST
from rest_framework.response import Response
from rest_framework import status, viewsets

# Models
from ping.models import Message

# Serializers
from ping.serializers import MessageSerializer

# dapi
from dapi.decoratores import resource


class RoomViewSet(viewsets.ViewSet):
    @resource
    def messages(self, request, serial=None):
        return Response(
            MessageSerializer(
                [
                    {'sender': m.sender.username,'body': m.body}
                    for m in Message.objects.filter(room__serial=serial)[:100]
                ],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )