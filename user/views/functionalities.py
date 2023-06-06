# Django
from django.contrib import messages
from django.contrib.admin.models import CHANGE
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
from django.shortcuts import redirect
# Helpers
from helpers.functions import log
# User
from user.decorators import is_authenticated, is_guest


@is_authenticated(False)
def cancel(request):
    if 'token' in request.session: del request.session['token']
    return redirect("home:index")

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
    log(
        request.user.id,
        request.user,
        CHANGE, 
        "signed out"
    )
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:user')

def navigate(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect("user:guest")
        else:
            return redirect("user:settings")
    return redirect("home:user")