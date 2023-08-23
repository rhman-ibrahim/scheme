# Django
from django.http import JsonResponse
from django.contrib import messages

# REST
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets

# Models
from team.models import Space
from ping.models import Message

# Helpers
from helpers.functions import secret

# Serializers
from .serializers import (
    MessageSerializer, SpaceSerializer, SpacePostSerializer
)

# dapi
from .decoratores import resource


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def flash(self, request):
        message_data = []
        for message in messages.get_messages(request):
            message_data.append({
                'body': message.message,
                'flag': message.tags,
            })
        return JsonResponse({'messages': message_data})
            

class SpaceViewSet(viewsets.ViewSet):

    @resource
    def info(self, request, pk=None):
        return Response(
            SpaceSerializer(Space.objects.get(id=pk)).data,
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        serializer = SpacePostSerializer(
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
                [
                    {'sender': m.sender.username,'body': m.body}
                    for m in Message.objects.filter(room__serial=serial)[:100]
                ],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )