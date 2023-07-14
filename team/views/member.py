# Django
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.admin.models import CHANGE, DELETION
# Helpers
from helpers.functions import log
# User
from user.decorators import is_authenticated
# Ping
from ping.models import Room
# Team
from team.models import Circle
from team.forms import CircleForm


@is_authenticated(True)
def leave(request):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    role   = circle.user_role(request.user)
    if role == "member":
        circle.members.remove(request.user)
        log(request.user.id, circle, CHANGE,
            f"left the circle ({circle.name})."
        )
        circle.save()
    elif role == "founder":
        log(request.user.id, circle, DELETION,
            f"deleted the circle ({circle.name})."
        )
        circle.delete()
    return redirect("team:close")

@is_authenticated(True)
def login(request, serial):
    circle = Circle.objects.get(serial=serial)
    role   = circle.user_role(request.user)
    if 'circle' in request.session:
        if circle.serial == request.session.get('circle'):
            return redirect("team:browse")
        else:
            messages.info(request, "close the opened circle")
            return redirect("user:navigate")
    else:
        if role != None:
            request.session['circle'] = circle.serial
            return redirect("team:browse")
        else:
            messages.warning(request, "you are not a member")
            return redirect("user:navigate")

@is_authenticated(True)
def logout(request):
    request.session.pop('circle')
    return redirect('user:navigate')

@is_authenticated(True)
def browse(request):
    if not 'circle' in request.session:
        return redirect("user:navigate")
    circle = Circle.objects.get(serial=request.session.get('circle'))
    return render(
        request,
        "team/index.html",
        {
            'forms': {
                'circle': CircleForm(instance=circle)
            },
            'circle': circle,
            'room': Room.objects.get(serial=circle.serial),
            'icons': {
                'left':"groups",
                "right":"forum"
            }
        }
    )