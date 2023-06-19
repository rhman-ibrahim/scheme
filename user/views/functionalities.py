# Django
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.models import CHANGE
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
from django.shortcuts import redirect
# Scheme
from scheme.settings import MEDIA_ROOT
# Helpers
from helpers.functions import log
# User
from user.decorators import is_authenticated, is_guest


def navigate(request):
    if request.user.is_authenticated:
        if request.user.is_guest: return redirect("user:guest")
        else: return redirect("user:settings")
    return redirect("home:user")

@is_authenticated(True)
@is_guest(False)
def token(request):
    with open(f"{MEDIA_ROOT}/user/tokens/{request.user.username}.png", 'rb') as f:
        file = f.read()
    response = HttpResponse(content_type='image/png')
    response.write(file)
    return response

@is_authenticated(True)
@is_guest(False)
def update_token(request):
    token = request.user.token
    if token != None:
        token.value = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:settings")

@is_authenticated(True)
def signout(request):
    if 'circle' in request.session:
        request.session.pop('circle')
    log(
        request.user.id,
        request.user,
        CHANGE, 
        "signed out"
    )
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:user')