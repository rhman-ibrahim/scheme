import uuid
from django.middleware.csrf import get_token
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from home.forms import SignUpForm, SignInForm
from rest_framework_simplejwt.tokens import RefreshToken
from helpers.functions import get_form_errors
from user.models import Account


class TokenViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def csrf(self, request):
        return Response(
            {'csrfToken', get_token(request)},
            status=status.HTTP_200_OK
        )


class AccountViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny]
    
    def signup(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            form.save()
            return Response(
                {'body': 'Your account has been created successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'body': get_form_errors(form)},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
    
    def signin(self, request):
        form = SignInForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response(
                {
                    'jwt': {
                        'access': str(access_token),
                        'refresh': str(refresh)
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'body': get_form_errors(form)},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    def signout(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response(
                {'body': 'Signed out successfully'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {'body': 'Something went wrong'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
    
    def temporary(self, request):
        user = Account.objects.create_guest(
            username = str(uuid.uuid4())[:8],
            password = str(uuid.uuid4())[:16]
        )
        refresh      = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response(
            {
                'jwt': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            },
            status=status.HTTP_200_OK
        )