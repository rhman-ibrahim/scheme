# Django
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors
# User
from user.decorators import is_authenticated, is_guest
from user.models import Account
# Mates
from mate.forms import AccountUsernameForm
from mate.models import FriendRequest


@is_authenticated(True)
@is_guest(False)
def create_friend_request(request):
    if request.method == "POST":
        form = AccountUsernameForm(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['username'] == request.user.username:
                    messages.info(
                        request,
                        "it is good to try to know yourself more, take some rest and meditate"
                    )
                    return redirect("user:back")
                account = Account.objects.get(username=form.cleaned_data['username'])
                FriendRequest.objects.create(
                    receiver = account,
                    sender   = request.user
                )
                messages.success(request, "friend request sent successfully")
            except Account.DoesNotExist:
                messages.error(request, "no account was found")
        else:
            get_form_errors(request, form)
    return redirect("user:back") 

@is_authenticated(True)
@is_guest(False)
def accept_friend_request(request, request_id):

    friend_request = FriendRequest.objects.get(
        id         = request_id,
        receiver   = request.user,
    )
    friend_request.status = True
    friend_request.save()
    friend_request.accept()
    
    return redirect("user:back")

@is_authenticated(True)
@is_guest(False)
def reject_friend_request(request, request_id):

    FriendRequest.objects.delete(
        id         = request_id,
        receiver   = request.user,
    )
    
    return redirect("user:back")

@is_authenticated(True)
@is_guest(False)
def delete_friend_request(request, request_id):

    FriendRequest.objects.delete(
        id     = request_id,
        sender = request.user 
    )
    
    return redirect("user:back")