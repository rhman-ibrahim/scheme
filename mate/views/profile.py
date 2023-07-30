# Django
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect, render
from django.contrib import messages

# Models
from django.db.models import Q
from mate.models import FriendRequest
from user.models import Account
from ping.models import Room

# Functions & Decorators
from helpers.functions import get_form_errors, log
from user.decorators import is_authenticated, is_guest


# Forms
from mate.forms import  ProfilePictureForm, ProfileInfoForm


@is_authenticated(True)
@is_guest(False)
def profile(request, username):
    try:
        instance  = Account.objects.get(username=username)
        friendsip = FriendRequest.objects.filter(
            (Q(receiver=instance) & Q(sender=request.user)) |
            (Q(sender=instance) & Q(receiver=request.user)) &
            Q(status=1)
        )
        if friendsip.exists():
            room = Room.objects.get(serial=friendsip.first().serial)
        else:
            messages.info(request, f"There is no connection with {username}")
            return redirect("user:back")
    except ObjectDoesNotExist:
        messages.info(request, f"There is no connection with {username}")
        return redirect("user:back")
    return render(
        request,
        "mate/index.html",
            {
                'mate': instance,
                'room': room,
                'column': {
                    'icon':'person'
                }
            }
        )

@is_authenticated(True)
@is_guest(False)
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile picture")
            messages.success(request, "profile picture updated successfully")
        else:
            get_form_errors(request, form)
    return redirect('user:back')

@is_authenticated(True)
@is_guest(False)
def update_profile_info(request):
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile info")
            messages.success(request, "profile info updated successfully")
        else:
            get_form_errors(request, form)
    return redirect('user:back')