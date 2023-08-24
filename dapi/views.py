# Django
from django.http import JsonResponse
from django.contrib import messages

# REST
from rest_framework.permissions import AllowAny
from rest_framework import viewsets



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