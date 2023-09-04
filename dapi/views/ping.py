from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import JsonResponse
from django.contrib import messages
from ping.models import Message
from dapi.decoratores import resource
from dapi.serializers.ping import MessageSerializer


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def flash(self, request):
        message_data = []
        for message in messages.get_messages(request):
            message_data.append(
                {
                    'body': message.message,
                    'flag': message.tags,
                }
            )
        return JsonResponse(
            {
                'messages': message_data
            }
        )


class RoomViewSet(viewsets.ViewSet):
    @resource
    def messages(self, request, identifier=None):
        return Response(
            MessageSerializer(
                [
                    {'sender': m.sender.username,'body': m.body}
                    for m in Message.objects.filter(room__identifier=identifier)[:100]
                ],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )