# Django
from django.utils.crypto import get_random_string
from django.contrib.admin.models import CHANGE
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.admin.models import LogEntry
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib import messages
# Scheme
from scheme.settings import MEDIA_ROOT
# Helpers
from helpers.functions import log
# Circles
from circles.forms import CircleForm
# User
from mates.forms import ProfilePictureForm, ProfileInfoForm
from user.decorators import is_authenticated, is_guest
from user.forms import  PasswordUpdateForm


@is_authenticated(True)
@is_guest(False)
def settings(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'circle': CircleForm
            },
            'logs': LogEntry.objects.filter(user=request.user),
            'icons': {
                'right':"diversity_2",
                'left':"history"
            }
        }
    )

def back(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def navigate(request):
    if request.user.is_authenticated:
        if request.user.is_guest: return redirect("user:guest")
        else: return redirect("user:settings")
    return redirect("home:index")

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
    return redirect('home:index')