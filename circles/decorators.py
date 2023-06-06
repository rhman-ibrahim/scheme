# Django
from django.contrib.admin.models import ADDITION, CHANGE
from django.shortcuts import render, redirect
from django.contrib import messages
# Circles
from circles.models import Circle
# User
from user.decorators import is_authenticated
from user.functions import log


# Check if there is an active circle's session
# Check if the requested circle and the session's circle are the same
# Check if the user is a founder
def circle_founder(view):
    def decorator(request, *args, **kwargs):
        requested_circle = Circle.objects.get(uuid=kwargs.get('serial'))
        if 'circle' in request.session:
            if requested_circle.id == request.session.get('circle'):
                session_circle = Circle.objects.get(id=request.session.get('circle'))
                if session_circle.user_role(request.user) == "founder":
                    return view(request, *args, **kwargs)
                else:
                    messages.warning(request, "you are not allowed to preform this action.")
                    return redirect("circles:page", kwargs.get('serial'))
            else:
                messages.warning(request, "you have to open the proper circle.")
                return redirect("circles:page", kwargs.get('serial'))
        else:
            messages.warning(request, "you have to open the circle.")
            return redirect("user:navigate")
    return decorator


# Check if there is an active circle's session
# Check if the requested circle and the session's circle are the same
# Check if the user is a member
def circle_member(view):
    def decorator(request, *args, **kwargs):
        requested_circle = Circle.objects.get(uuid=kwargs.get('serial'))
        if 'circle' in request.session:
            if requested_circle.id == request.session.get('circle'):
                session_circle = Circle.objects.get(id=request.session.get('circle'))
                if session_circle.user_role(request.user) != None:
                    return view(request, *args, **kwargs)
                else:
                    messages.warning(request, "you are not allowed to preform this action.")
                    return redirect("user:navigate")
            else:
                messages.warning(request, "you have to open the proper circle.")
                return redirect("user:navigate")
        else:
            messages.warning(request, "you have to open the circle.")
            return redirect("user:navigate")
    return decorator