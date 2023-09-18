from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from home.forms import SignUpForm, SignInForm
from django.middleware.csrf import get_token



class TokenViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    
    def csrf(self, request):
        return Response({'csrfToken', get_token(request)}, status=status.HTTP_200_OK)

class AccountViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny]
    
    def signup(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            form.save()
            return Response(
                {'message': 'Your account has been created successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'messages': form.errors},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
    
    def signin(self, request):
        form = SignInForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            response = Response(
                {'token': user.token.key},
                status=status.HTTP_200_OK
            )
            response.set_cookie('ping', "pong", samesite=None, secure=False, httponly=False)
            return response
        else:
            return Response(
                {'messages': form.errors},
                status=status.HTTP_401_UNAUTHORIZED
            )