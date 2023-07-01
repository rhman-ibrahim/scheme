from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MessageSerializer
from .models import Message

@api_view(['GET'])
def room_messages(request, serial):
    messages   = [
        {'body':message.body, 'sender':message.sender.username}
        for message in Message.objects.filter(room__space=serial)[:100]
    ]
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)