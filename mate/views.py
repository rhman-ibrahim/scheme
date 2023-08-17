# Django
from django.shortcuts import render
from django.contrib import messages

# Models
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.db.models import Q

# Errors
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Models
from mate.models import FriendRequest
from user.models import Account
from ping.models import Room

# Forms
from mate.forms import (
    AccountUsernameForm, ProfileInfoForm,
    ProfilePictureForm
)

# Decorators
from helpers.decorators import (
    back,
    is_authenticated,
    is_guest
)

# Functions
from helpers.functions import (
    get_form_errors,
    log
)


@is_authenticated(True)
@back
def create_request(request):
    if request.method == "POST":
        try:
            form = AccountUsernameForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['username'] == request.user.username:
                    messages.info(
                        request,
                        "it is good to try to know yourself more, take some rest and meditate"
                    )
                account = Account.objects.get(username=form.cleaned_data['username'])
                f_req   = FriendRequest.objects.create(receiver=account, sender=request.user)
                messages.success(
                    request,
                    f"friend request was sent successfully to {account.username}"
                )
                log(
                    request.user.id, f_req, ADDITION,
                    f"sent {account.username} a friend request"
                )
        except ValidationError as e:
            messages.error(
                request,
                e.messages[0]
            )
        except IntegrityError:
            messages.warning(
                request,
                "you can't send this user a friend request"
            )
            messages.info(
                request,
                "there is a pending or a previous request"
            )
        else: get_form_errors(request, form)


@is_authenticated(True)
@back
def retrieve_mate_index(request, username):
    mate      = Account.objects.get(username=username)
    friendsip = FriendRequest.objects.get(
        (Q(sender=request.user) & Q(receiver=mate)) |
        (Q(sender=mate) & Q(receiver=request.user)) &
        Q(status=1)
    )
    if friendsip.exists():
        room = Room.objects.get(serial=friendsip.get(status=1).serial)
        return render(
            request,
            "mate/index.html",
            {
                'mate': mate,
                'room': room,
                'column': {
                    'icon':'format_quote'
                }
            }
        )


@is_authenticated(True)
@is_guest(False)
@back
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

@is_authenticated(True)
@is_guest(False)
@back
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

@is_authenticated(True)
@back
def accept_request(request, req):
    friend_request = FriendRequest.objects.get(id=req)
    if request.user == friend_request.receiver:
        friend_request.status = 1
        friend_request.save()
        messages.success(request, f"Now you are friends with {friend_request.sender.username}")
        log(
            request.user.id, friend_request, CHANGE,
            f"accepted the friend request received from {friend_request.sender.username}"
        )
    else:
        messages.warning(
            request,
            "you are not allowed to perform this action"
        )

@is_authenticated(True)
@back
def reject_request(request, req):
    friend_request = FriendRequest.objects.get(id=req)
    if request.user == friend_request.receiver:
        friend_request.status = 0
        friend_request.save()
        messages.success(
            request,
            f"You have rejected {friend_request.sender.username}'s friend request"
        )
        log(
            request.user.id, friend_request, CHANGE,
            f"rejected the friend request received from {friend_request.sender.username}"
        )
    else:
        messages.warning(
            request,
            "you are not allowed to perform this action"
        )

@is_authenticated(True)
@back
def delete_request(request, req):
    friend_request = FriendRequest.objects.get(id=req)
    if request.user == friend_request.sender:
        friend_request.delete()
        messages.success(
            request,
            f"you have cancelled the friend request to {friend_request.receiver.username}"
        )
        log(
            request.user.id, friend_request, DELETION,
            f"deleted the friend request sent to {friend_request.receiver.username}"
        )
    else:
        messages.warning(
            request,
            "you are not allowed to perform this action"
        )