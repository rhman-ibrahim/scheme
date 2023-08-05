import datetime, timeago
from django.utils.timezone import utc
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from user.models import Account
import pytz


def is_authenticated(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            else:
                if status:
                    messages.warning(request, "you have to signin first.")
                    return redirect("home:index")
                else:
                    messages.warning(request, "you have to signout first.")
                return redirect('user:nav')
        return wrapper
    return decorator

def is_guest(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_guest:
                return view(request, *args, **kwargs)
            else:
                if status: messages.warning(request, "Only guest users are allowed to view this.")
                messages.warning(request, "Guest users are not allowed to view this.")
                return redirect('user:settings')
        return wrapper
    return decorator

def track_guest(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_guest:
            termination = request.user.termination
            if termination['state']:
                return redirect("user:terminate")
        return view(request, *args, **kwargs)
    return wrapper