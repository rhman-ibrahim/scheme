# Django
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages

# Models
from user.models import Account
from team.models import Space
from .models import FriendRequest, SpaceRequest

# Forms
from mate.forms import RequestForm

# Decorators
from helpers.decorators import (
    back,
    is_authenticated,
    is_founder, is_logined,
)

# Functions
from helpers.functions import (
    get_form_errors,
    create_a_guest_account,
)


@is_authenticated(True)
@back
def create_friend_request(request):
    if request.method == "POST":
        try:
            form = RequestForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['identifier'] == request.user.username:
                    messages.info(request, "it is good to try to know yourself more, take some rest and meditate")
                else:
                    FriendRequest.objects.create(
                        receiver=Account.objects.get(username=form.cleaned_data['identifier']),
                        message=form.cleaned_data['message'],
                        sender=request.user
                    )
                    messages.success(request, f"friend request was sent successfully to {form.cleaned_data['identifier']}")
        except ValidationError as e:
            messages.error(request, e.messages[0] )
        except IntegrityError:
            messages.warning(request, "you can't send this user a friend request")
            messages.info(request, "there is a pending or a previous request")
        else:
            get_form_errors(request, form)

@back
def create_space_request(request):
    if not request.user.is_authenticated:
        create_a_guest_account(request)
    if request.method == 'POST':
        form  = RequestForm(request.POST)
        if form.is_valid():
            query  = SpaceRequest.objects.filter(space__identifier=form.cleaned_data['identifier'], user=request.user)
            if query.exists():
                sreq = query.first()
                if sreq.status == 2:
                    messages.info(request, f"Your request to join this space is pending")
                elif sreq.status == 1:
                    messages.info(request, f"You are already connected to this space")
            else:
                SpaceRequest.objects.create(
                    space=Space.objects.get(identifier=form.cleaned_data['identifier']),
                    user=request.user
                )
                messages.success(request, "join request created successfully.")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@back
def accept_friend_request(request, id):
    friend_request = FriendRequest.objects.get(id=id)
    if request.user == friend_request.receiver:
        friend_request.accept()
        messages.success(request, f"Now you are friends with {friend_request.sender.username}")
    else:
        messages.warning(request,"you are not allowed to perform this action")

@is_authenticated(True)
@back
def reject_friend_request(request, id):
    freq = FriendRequest.objects.get(id=id)
    if request.user == freq.receiver:
        freq.reject()
        messages.success(request,f"You have rejected {freq.sender.username}'s friend request")
    else:
        messages.warning(request,"you are not allowed to perform this action")

@is_authenticated(True)
@back
def delete_friend_request(request, id):
    freq = FriendRequest.objects.get(id=id)
    if request.user == freq.sender:
        freq.cancel()
        messages.success(request,f"you have cancelled the sent request to {freq.receiver.username}")
    else:
        messages.warning(request,"you are not allowed to perform this action")

@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def accept_space_request(request, id):
    sreq = SpaceRequest.objects.get(id=id)
    sreq.accept()
    
@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def reject_space_request(request, id):
    sreq = SpaceRequest.objects.get(id=id)
    sreq.reject()
    
@is_authenticated(True)
@is_logined(True)
@back
def delete_space_request(request, id):
    sreq = SpaceRequest.objects.get(id=id)
    if request.user == sreq.user:
        sreq.cancel()
        messages.warning(request,"You are not allowed to preform this action")