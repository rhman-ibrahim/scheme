# Django
from django.shortcuts import render, redirect
from django.contrib.admin.models import CHANGE
# Ping
from ping.models import Room
# User
from user.decorators import is_authenticated
from user.functions import log
# Team
from team.models import Circle, CircleRequest


@is_authenticated(True)
def approve(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 1
    c_req.circle.members.add(c_req.user)
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"approved ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    return redirect("team:browse")
    
@is_authenticated(True)
def reject(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 0
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"rejected ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    return redirect("team:browse")

@is_authenticated(True)
def remove(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user   = circle.members.get(id=int(user_id))
    circle.members.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"removed ({user.username}) from the circle ({circle.name})."
    )
    return redirect("team:browse")