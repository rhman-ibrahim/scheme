# REST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Model
from ping.models import Message

# Serializers
from .serializers import MessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_room_messages(request, serial):
    serializer = MessageSerializer(
        [
            {
                'sender': message.sender.username,
                'body': message.body
            }
            for message in Message.objects.filter(room__serial=serial)[:100]
        ],
        many=True
    )
    return Response(serializer.data)