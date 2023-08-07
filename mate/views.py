# Django
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
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
from helpers.decorators import back, home
from user.decorators import (
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
        except Account.DoesNotExist:
            messages.error(request, "no account was found")

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
# @back
def retrieve_mate_index(request, username):
    try:
        mate      = Account.objects.get(username=username)
        friendsip = FriendRequest.objects.filter(
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
    except ObjectDoesNotExist:
        messages.info(request, f"There is no connection with {username}")


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
    f_req        = FriendRequest.objects.get(id=req)
    f_req.status = 1
    f_req.save()
    messages.success(request, f"Now you are friends with {f_req.sender.username}")
    log(request.user.id, f_req, CHANGE,
        f"accepted the friend request received from {f_req.sender.username}"
    )

@is_authenticated(True)
@back
def reject_request(request, req):
    f_req        = FriendRequest.objects.get(id=req)
    f_req.status = 0
    f_req.save()
    messages.success(
        request,
        f"You have rejected {f_req.sender.username}'s friend request"
    )
    log(request.user.id, f_req, CHANGE,
        f"rejected the friend request received from {f_req.sender.username}"
    )

@is_authenticated(True)
@back
def delete_request(request, req):
    f_req = FriendRequest.objects.get(id=req)
    f_req.delete()
    messages.success(
        request,
        f"You have cancelled the friend request to {f_req.receiver.username}"
    )
    log(request.user.id, f_req, DELETION,
        f"deleted the friend request sent to {f_req.receiver.username}"
    )