
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from user.models import Token
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def signup(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Your account has been created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def signin(self, request):
        if request.data.get('username') == None or request.data.get('password') == None:
            return Response(
                {'message': 'HTTP_400_BAD_REQUEST'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            if user is not None:
                return Response(
                    {'token': Token.objects.get(user=user).key},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'HTTP_401_UNAUTHORIZED'},
                    status=status.HTTP_401_UNAUTHORIZED
                )