# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# Models
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.db.models import Q

# Errors
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Models
from user.models import Account
from team.models import Circle
from ping.models import Room
from .models import FriendRequest, CircleRequest

# Forms
from mate.forms import AccountUsernameForm, CircleRequestForm

# Decorators
from helpers.decorators import (
    back,
    is_authenticated,
    is_founder,
    is_logined,
)

# Functions
from helpers.functions import (
    get_form_errors,
    log
)


@is_authenticated(True)
@back
def create_friend_request(request):
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
@back
def accept_friend_request(request, req):
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
def reject_friend_request(request, req):
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
def delete_friend_request(request, req):
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


@back
def create_circle_request(request):
    if request.method == 'POST':
        form  = CircleRequestForm(request.POST)
        if form.is_valid():
            circle          = Circle.objects.get(serial=form.cleaned_data['serial'])
            circle_request  = CircleRequest.objects.get(circle=circle, user=request.user)
            if circle_request.status == 2:
                messages.info(request, f"Your request to join {circle.name} is pending")
            elif circle_request.status == 1:
                messages.info(request, f"You are already connected to {circle.name}")
            else:
                CircleRequest.objects.create(
                    circle=circle,
                    user=request.user
                )
                messages.success(
                    request,
                    "join request created successfully."
                    )
                log(
                    request.user.id, circle, ADDITION,
                    f"requested to join the circle ({circle.name})."
                )
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def accept_circle_request(request, user_id):
    c_req        = CircleRequest.objects.get(circle__id=request.session.get('circle'), user__id=user_id)
    c_req.status = 1
    c_req.circle.members.add(c_req.user)
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"approved ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    
@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def reject_circle_request(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 0
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"rejected ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    
@is_authenticated(True)
@is_logined(True)
@back
def delete_circle_request(request, request_id):
    circle_request = CircleRequest.objects.get(id=request_id)
    if request.user == circle_request.user:
        circle_request.delete()
        log(
            request.user.id, circle_request.circle, DELETION,
            f"approved ({circle_request.user.username}) joining the circle ({circle_request.circle.name})."
        )
        messages.warning(
            request,
            "You are not allowed to preform this action"
        )
        return redirect("team:retrieve_team_index")