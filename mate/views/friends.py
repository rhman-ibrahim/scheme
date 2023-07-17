# Django
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.shortcuts import redirect
from django.contrib import messages

# Functions & Decorators
from user.decorators import is_authenticated, is_guest
from helpers.functions import get_form_errors, log

# Models
from mate.models import FriendRequest
from user.models import Account

# Forms
from mate.forms import AccountUsernameForm


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
                f_req   = FriendRequest.objects.create(
                    receiver=account,
                    sender=request.user
                )
                
                messages.success(
                    request,
                    f"friend request was sent successfully to {account.username}"
                )

                log(request.user.id, f_req, ADDITION,
                    f"sent {account.username} a friend request"
                )

            except Account.DoesNotExist:
                messages.error(request, "no account was found")
        else:
            get_form_errors(request, form)
    return redirect("user:back") 

@is_authenticated(True)
@is_guest(False)
def accept_friend_request(request, req):

    f_req        = FriendRequest.objects.get(id=req)
    f_req.status = 1
    f_req.save()

    messages.success(request, f"Now you are friends with {f_req.sender.username}")

    log(request.user.id, f_req, CHANGE,
        f"accepted the friend request received from {f_req.sender.username}"
    )

    return redirect("user:back")

@is_authenticated(True)
@is_guest(False)
def reject_friend_request(request, req):

    f_req        = FriendRequest.objects.get(id=req)
    f_req.status = 0
    f_req.save()

    messages.success(request, f"You have rejected {f_req.sender.username}'s friend request")
    
    log(request.user.id, f_req, CHANGE,
        f"rejected the friend request received from {f_req.sender.username}"
    )

    return redirect("user:back")

@is_authenticated(True)
@is_guest(False)
def delete_friend_request(request, req):

    f_req = FriendRequest.objects.get(id=req)
    f_req.delete()

    messages.success(request, f"You have cancelled the friend request to {f_req.receiver.username}")

    log(request.user.id, f_req, DELETION,
        f"deleted the friend request sent to {f_req.receiver.username}"
    )
    
    return redirect("user:back")